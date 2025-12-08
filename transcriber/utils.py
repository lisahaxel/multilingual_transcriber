import os
import sys
import logging
import subprocess
import base64
from pathlib import Path
from typing import Optional, Tuple
from .config import EXTENSIONS, LOG_FORMAT, LOG_LEVEL

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
log = logging.getLogger(__name__)

def setup_environment():
    """Sets necessary environment variables for optimal performance."""
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['KMP_WARNINGS'] = '0'

def get_file_type(path: Path) -> Optional[str]:
    """Determines file category based on extension."""
    ext = path.suffix.lower()
    for ftype, extensions in EXTENSIONS.items():
        if ext in extensions:
            return ftype
    return None

def extract_audio_from_video(video_path: Path) -> Optional[str]:
    """Extracts MP3 audio from video using FFmpeg."""
    output = (video_path.parent / f"{video_path.stem}_audio.mp3").resolve()
    log.info("Extracting audio from video...")
    try:
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path.resolve()), '-vn', 
            '-acodec', 'libmp3lame', '-b:a', '128k', '-ac', '1', str(output)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return str(output)
    except subprocess.CalledProcessError as e:
        log.error(f"FFmpeg extraction failed: {e}")
    except FileNotFoundError:
        log.error("FFmpeg not found. Please install FFmpeg.")
    return None

def normalize_audio(file_path: Path) -> str:
    """Normalizes audio volume using FFmpeg. Returns absolute path."""
    file_path = file_path.resolve()
    output = file_path.parent / f"{file_path.stem}_normalized.mp3"
    output = output.resolve()
    
    log.info("Normalizing audio...")
    try:
        cmd = [
            'ffmpeg', '-y', '-i', str(file_path), '-af', 'volume=1.5',
            '-codec:a', 'libmp3lame', '-b:a', '128k', '-ac', '1', str(output)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return str(output)
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("Audio normalization skipped (FFmpeg not available or error).")
        return str(file_path)

def encode_audio_base64(audio_path: str) -> Tuple[str, str]:
    """Reads audio file and returns base64 string and mime type."""
    audio_path = str(Path(audio_path).resolve())
    
    ext = Path(audio_path).suffix.lower()
    mime = {'.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.m4a': 'audio/mp4'}.get(ext, 'audio/mpeg')
    with open(audio_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return data, mime

def format_timestamp(seconds: float) -> str:
    """Formats seconds into MM:SS string."""
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"
