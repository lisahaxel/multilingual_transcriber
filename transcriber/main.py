import argparse
import json
import os
import re
import logging
from pathlib import Path

# Local imports
from . import config, utils, parsers, core, templates

log = logging.getLogger(__name__)

class Processor:
    def __init__(self, args):
        self.args = args
        self.nlp = core.NLPProcessor()
        self.transcriber = None
        
        # Initialize transcriber only if needed
        self.files = self._gather_files()
        has_audio = any(utils.get_file_type(f) in ('audio', 'video') for f in self.files)
        
        if has_audio:
            self.transcriber = core.Transcriber(args.model)

    def _gather_files(self):
        candidates = []
        for inp in self.args.input:
            path = Path(inp).resolve()  # Use absolute paths
            if path.is_dir():
                for cat, exts in config.EXTENSIONS.items():
                    for ext in exts:
                        candidates.extend(sorted(path.glob(f"*{ext}")))
            elif path.exists():
                candidates.append(path)
        
        # Filter out any _normalized or _audio temp files
        candidates = [f for f in candidates if '_normalized.' not in f.name and '_audio.' not in f.name]
                
        # Filter processed unless force
        queue = []
        tgt_esc = re.escape(self.args.target)
        for f in candidates:
            if self.args.force:
                queue.append(f)
                continue
            # Check existing pattern
            pat = re.compile(re.escape(f.stem) + r'_[a-zA-Z]+-' + tgt_esc + r'_interactive\.html')
            if not any(pat.fullmatch(p.name) for p in f.parent.iterdir() if p.is_file()):
                queue.append(f)
                
        if self.args.limit:
            queue = queue[:self.args.limit]
            
        return queue

    def run(self):
        log.info(f"Processing {len(self.files)} files...")
        for i, f in enumerate(self.files):
            log.info(f"[{i+1}/{len(self.files)}] Processing: {f.name}")
            try:
                self._process_file(f)
            except Exception as e:
                log.error(f"Failed to process {f.name}: {e}", exc_info=True)

    def _process_file(self, path):
        ftype = utils.get_file_type(path)
        if ftype in ('audio', 'video'):
            self._handle_media(path, ftype)
        elif ftype == 'text':
            self._handle_text(path)

    def _handle_media(self, path, ftype):
        temp_files = []
        audio_path = str(path.resolve())  # Use absolute path
        
        if ftype == 'video':
            audio_path = utils.extract_audio_from_video(path)
            if not audio_path:
                return
            temp_files.append(audio_path)
            
        normalized = utils.normalize_audio(Path(audio_path))
        if normalized != audio_path:
            temp_files.append(normalized)
        
        transcribe_path = normalized
            
        # Transcribe
        src_lang = self.args.source 
        res, _, detected = self.transcriber.transcribe(transcribe_path, src_lang)
        actual_src = src_lang or detected
        
        # Prepare Data
        segments = []
        texts = []
        if isinstance(res, dict):
             segs_raw = res.get('segments', [])
        else:
             segs_raw = getattr(res, 'segments', [])

        prev_text = None
        for s in segs_raw:
            # Normalize structure between backends
            if isinstance(s, dict):
                start, end, text, words = s['start'], s['end'], s['text'], s.get('words', [])
            else:
                start, end, text, words = s.start, s.end, s.text, getattr(s, 'words', [])

            # Skip empty segments
            text_stripped = text.strip() if text else ''
            if not text_stripped:
                continue
            
            # Skip segments with Unicode replacement characters (garbage)
            if '\ufffd' in text_stripped or '�' in text_stripped:
                continue
            
            # Skip hallucinated repetitive content (Whisper loop artifacts)
            text_words = text_stripped.split()
            if len(text_words) > 5:
                unique_words = set(text_words)
                if len(unique_words) <= 2 and len(text_words) > 10:
                    log.debug(f"Skipping repetitive hallucination: {text_stripped[:50]}...")
                    continue
            
            latin_chars = sum(1 for c in text_stripped if c.isalpha() and ord(c) < 0x250)
            non_latin_chars = sum(1 for c in text_stripped if c.isalpha() and ord(c) >= 0x250)
            
            if non_latin_chars > latin_chars and non_latin_chars > 5:
                log.debug(f"Skipping wrong-script hallucination: {text_stripped[:50]}...")
                continue

            cleaned_words = []
            if words:
                for w in words:
                    # Handle different word object structures (dict, object, or string)
                    if isinstance(w, dict):
                        wt = w.get('word', w.get('text', ''))
                        ws = w.get('start', 0)
                        we = w.get('end', 0)
                    elif isinstance(w, str):
                        wt = w
                        ws = 0
                        we = 0
                    else:
                        wt = getattr(w, 'word', getattr(w, 'text', ''))
                        ws = getattr(w, 'start', 0)
                        we = getattr(w, 'end', 0)
                    wt_stripped = wt.strip() if wt else ''
                    # Skip empty words
                    if wt_stripped:
                        cleaned_words.append({'text': wt_stripped, 'start': ws, 'end': we})

            # Skip consecutive exact duplicates (common MLX-Whisper artifact)
            normalized = re.sub(r'[^\w\s]', '', text_stripped.lower()).strip()
            prev_normalized = re.sub(r'[^\w\s]', '', prev_text.lower()).strip() if prev_text else None
            
            if normalized == prev_normalized and start < 10.0:
                # Skip this duplicate, but update prev_text
                prev_text = text_stripped
                continue

            seg = {
                'start': start, 'end': end,
                'timestamp': utils.format_timestamp(start),
                'source': text_stripped,
                'words': cleaned_words
            }
            segments.append(seg)
            texts.append(seg['source'])
            prev_text = text_stripped

        # Translate & Build Vocab
        translations = self.nlp.translate_batch(texts, actual_src, self.args.target)
        for i, s in enumerate(segments):
            s['translation'] = translations[i]
            
        word_info = self.nlp.build_vocabulary(segments, actual_src, self.args.target)
        
        # Generate HTML - use original path for output naming
        output = path.parent / f"{path.stem}_{actual_src}-{self.args.target}_interactive.html"
        audio_b64, mime = utils.encode_audio_base64(transcribe_path)
        
        footer = "Transcribed with Whisper"
        if actual_src != self.args.target:
            footer += " · Translated with Google"
        
        html = templates.get_av_html(
            actual_src, config.LANGUAGES.get(actual_src, actual_src),
            config.LANGUAGES.get(self.args.target, self.args.target),
            path.name, audio_b64, mime,
            json.dumps(segments, ensure_ascii=False),
            json.dumps(word_info, ensure_ascii=False),
            re.sub(r'[^\w\-]', '_', path.stem)[:30],
            self.args.target, footer
        )
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(html)
            
        # Cleanup temp files
        for t in temp_files:
            try:
                if os.path.exists(t):
                    os.remove(t)
            except Exception as e:
                log.debug(f"Failed to remove temp file {t}: {e}")
        
        log.info(f"Created: {output.name}")

    def _handle_text(self, path):
        if not self.args.source:
            log.error(f"Source language (-s) is required for text file: {path.name}")
            return

        raw_segs = parsers.TextParser.parse(path)
        segments = []
        texts = []
        
        for i, s in enumerate(raw_segs):
            seg = {
                'start': s['start'], 'end': s['end'],
                'timestamp': str(i+1),
                'source': s['text'],
                'words': [{'text': w, 'start':0, 'end':0} for w in s['text'].split()]
            }
            segments.append(seg)
            texts.append(seg['source'])
            
        translations = self.nlp.translate_batch(texts, self.args.source, self.args.target)
        for i, s in enumerate(segments):
            s['translation'] = translations[i]
            
        word_info = self.nlp.build_vocabulary(segments, self.args.source, self.args.target)
        
        output = path.parent / f"{path.stem}_{self.args.source}-{self.args.target}_interactive.html"
        footer = "Translated with Google"
        
        html = templates.get_text_html(
            self.args.source, config.LANGUAGES.get(self.args.source, self.args.source),
            config.LANGUAGES.get(self.args.target, self.args.target),
            path.name,
            json.dumps(segments, ensure_ascii=False),
            json.dumps(word_info, ensure_ascii=False),
            re.sub(r'[^\w\-]', '_', path.stem)[:30],
            self.args.target, footer
        )
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(html)
            
        log.info(f"Created: {output.name}")

def main():
    utils.setup_environment()
    
    parser = argparse.ArgumentParser(
        description='Generate interactive HTML transcripts from media or text.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', nargs='*', help='Input file(s) or directory')
    parser.add_argument('-s', '--source', help='Source language (required for text files)')
    parser.add_argument('-t', '--target', default='en', help='Target language (default: en)')
    parser.add_argument('-m', '--model', default=None, help='Whisper model (auto-detected based on backend)')
    parser.add_argument('-n', '--limit', type=int, help='Process only N files')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing outputs')
    parser.add_argument('--list-languages', action='store_true', help='Show available languages')
    
    args = parser.parse_args()

    if args.list_languages:
        print("Supported Languages:")
        for k, v in sorted(config.LANGUAGES.items()):
            print(f"  {k}: {v}")
        return

    if not args.input:
        parser.print_help()
        return

    Processor(args).run()

if __name__ == "__main__":
    main()
