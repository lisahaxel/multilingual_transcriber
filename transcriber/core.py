import sys
import time
import re
import subprocess
import logging
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import SPACY_MODELS, LANG_ALIASES

log = logging.getLogger(__name__)

# Default models per backend
DEFAULT_MODELS = {
    'mlx': 'mlx-community/whisper-large-v3-turbo',
    'faster': 'large-v3-turbo',
    'standard': 'large-v3-turbo',
}

class Transcriber:
    """Wrapper for multiple Whisper backends (MLX, Faster-Whisper, OpenAI)."""
    
    def __init__(self, model_path: str = None):
        self._model = None
        self._backend = self._detect_backend()
        self.model_path = self._resolve_model_path(model_path)
        self._setup_device()

    def _detect_backend(self):
        try:
            import mlx_whisper
            self.lib = mlx_whisper
            return 'mlx'
        except ImportError: pass
        
        try:
            import faster_whisper
            self.lib = faster_whisper
            return 'faster'
        except ImportError: pass
        
        try:
            import whisper
            self.lib = whisper
            return 'standard'
        except ImportError:
            log.error("No Whisper backend found. Install mlx-whisper, faster-whisper, or openai-whisper.")
            sys.exit(1)

    def _resolve_model_path(self, model_path: str) -> str:
        """Resolve the correct model path based on backend."""
        if not model_path:
            return DEFAULT_MODELS[self._backend]
        
        if 'mlx' in model_path.lower() and self._backend != 'mlx':
            log.warning(f"MLX model '{model_path}' not compatible with {self._backend} backend.")
            log.info(f"Using default model: {DEFAULT_MODELS[self._backend]}")
            return DEFAULT_MODELS[self._backend]
    
        if 'mlx' not in model_path.lower() and self._backend == 'mlx':
            log.warning(f"Model '{model_path}' not compatible with MLX backend.")
            log.info(f"Using default MLX model: {DEFAULT_MODELS['mlx']}")
            return DEFAULT_MODELS['mlx']
        
        return model_path

    def _setup_device(self):
        if self._backend == 'mlx':
            log.info("Backend: MLX-Whisper (Apple Silicon)")
                
        elif self._backend == 'faster':
            import torch
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.compute_type = 'float16' if self.device == 'cuda' else 'int8'
            log.info(f"Backend: Faster-Whisper ({self.device.upper()})")
        else:
            import torch
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            log.info(f"Backend: Standard Whisper ({self.device.upper()})")

    def transcribe(self, audio_path: str, lang: str = None):
        log.info(f"Transcribing {audio_path}...")
        start_time = time.time()
        
        # --- MLX BACKEND ---
        if self._backend == 'mlx':
            params = {
                'word_timestamps': True,
                'verbose': False,
                'path_or_hf_repo': self.model_path,
                'condition_on_previous_text': False,
                'no_speech_threshold': None,
                'compression_ratio_threshold': 2.4,
            }
            if lang:
                params['language'] = lang

            res = self.lib.transcribe(audio_path, **params)
            detected = res.get('language', lang)
            return res, time.time() - start_time, detected

        # --- FASTER WHISPER BACKEND ---
        if self._backend == 'faster':
            if not self._model:
                self._model = self.lib.WhisperModel(self.model_path, device=self.device, compute_type=self.compute_type)
            
            segments, info = self._model.transcribe(
                audio_path, 
                language=lang, 
                word_timestamps=True,
                condition_on_previous_text=False, 
                no_speech_threshold=None,
                log_prob_threshold=None, 
                compression_ratio_threshold=2.4, 
                beam_size=5
            )
            
            results = []
            full_text = []
            for s in segments:
                words = [{'word': w.word, 'start': w.start, 'end': w.end} for w in s.words] if s.words else []
                results.append({
                    'start': s.start, 'end': s.end, 'text': s.text, 'words': words, 'id': s.id
                })
                full_text.append(s.text)
            
            return {'segments': results, 'text': ''.join(full_text)}, time.time() - start_time, info.language

        # --- STANDARD WHISPER FALLBACK ---
        if not self._model:
            self._model = self.lib.load_model(self.model_path, device=self.device)
            
        params = {
            'word_timestamps': True, 
            'verbose': False, 
            'temperature': [0.0, 0.2, 0.4],
            'condition_on_previous_text': False, 
            'no_speech_threshold': None,
            'logprob_threshold': None, 
            'compression_ratio_threshold': 2.4,
            'fp16': (self.device=='cuda'), 
            'beam_size': 5
        }
        if lang:
            params['language'] = lang
            
        res = self._model.transcribe(audio_path, **params)
        return res, time.time() - start_time, res.get('language', lang)


class NLPProcessor:
    """Handles Translation and Lemmatization."""
    
    def __init__(self):
        self._spacy_cache = {}
        self.voikko = self._load_voikko()
        self.translator_cls = self._load_translator()
        self.spacy_lib = self._load_spacy()

    def _load_voikko(self):
        # Voikko requires native DLLs that are not available via pip on Windows
        # On Windows, fall back to spaCy for Finnish lemmatization
        if platform.system() == 'Windows':
            log.info("Windows detected: using spaCy for Finnish lemmatization (Voikko not supported).")
            return None
        
        try:
            import libvoikko
            voikko_instance = libvoikko.Voikko('fi')
            # Test that it actually works
            voikko_instance.analyze('testi')
            log.info("Voikko loaded for Finnish lemmatization.")
            return voikko_instance
        except Exception as e:
            log.info(f"Voikko not available: {e}. Using spaCy for Finnish instead.")
            return None

    def _load_translator(self):
        try:
            from deep_translator import GoogleTranslator
            return GoogleTranslator
        except ImportError:
            log.warning("deep-translator not found. Translation disabled.")
            return None

    def _load_spacy(self):
        try:
            import spacy
            return spacy
        except ImportError: return None

    def _get_spacy_model(self, lang):
        if lang in self._spacy_cache: return self._spacy_cache[lang]
        model_name = SPACY_MODELS.get(lang)
        if not model_name or not self.spacy_lib: return None
        
        try:
            nlp = self.spacy_lib.load(model_name)
            self._spacy_cache[lang] = nlp
            return nlp
        except OSError:
            log.info(f"Downloading SpaCy model: {model_name}...")
            subprocess.run([sys.executable, '-m', 'spacy', 'download', model_name], check=True, capture_output=True)
            nlp = self.spacy_lib.load(model_name)
            self._spacy_cache[lang] = nlp
            return nlp

    def lemmatize(self, word: str, lang: str) -> str:
        word = re.sub(r'[^\w\-]', '', word).strip()
        if not word: return None
        
        lang = LANG_ALIASES.get(lang, lang)
        
        # Finnish: use Voikko if available (macOS/Linux), otherwise fall back to spaCy
        if lang == 'fi' and self.voikko:
            try:
                a = self.voikko.analyze(word)
                if a: return a[0].get('BASEFORM')
            except: pass
            
        # SpaCy for all languages (including Finnish on Windows)
        nlp = self._get_spacy_model(lang)
        if nlp:
            try:
                doc = nlp(word)
                if doc: return doc[0].lemma_
            except: pass
            
        return None

    def translate_batch(self, texts: list, src: str, tgt: str, max_workers=10) -> list:
        if not self.translator_cls or src == tgt:
            return texts if src == tgt else [''] * len(texts)
            
        log.info(f"Translating {len(texts)} segments ({src}->{tgt})...")
        results = [None] * len(texts)
        
        def _task(idx, text):
            if not text.strip(): return idx, ''
            t = self.translator_cls(source=src, target=tgt)
            for _ in range(3): # Retry logic
                try: return idx, t.translate(text.strip())
                except: time.sleep(0.3)
            return idx, '[Error]'

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_task, i, txt): i for i, txt in enumerate(texts)}
            for f in as_completed(futures):
                try:
                    i, res = f.result()
                    results[i] = res
                except: pass
        return results

    def build_vocabulary(self, segments, src, tgt):
        words = set()
        for s in segments:
            for w in s.get('words', []):
                clean = re.sub(r'[^\w\-]', '', w['text']).strip().lower()
                if len(clean) > 1: words.add(clean)
                
        log.info(f"Building vocabulary ({len(words)} words)...")
        vocab = {}
        
        # Lemmatize
        for w in words:
            base = self.lemmatize(w, src) or w
            vocab[w] = {'baseform': base, 'translation': None}
            
        # Translate baseforms
        if self.translator_cls and src != tgt:
            def _trans(w, base):
                try: return w, self.translator_cls(source=src, target=tgt).translate(base)
                except: return w, None
                
            with ThreadPoolExecutor(max_workers=10) as pool:
                futures = [pool.submit(_trans, w, vocab[w]['baseform']) for w in words]
                for f in as_completed(futures):
                    w, t = f.result()
                    if t: vocab[w]['translation'] = t
                    
        return vocab
