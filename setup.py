from setuptools import setup, find_packages

setup(
    name="multilingual-transcriber",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies (always installed)
        "deep-translator",
        "beautifulsoup4",
        "pymupdf",
        "spacy",
    ],
    extras_require={
        # Apple Silicon (M1/M2/M3/M4)
        "mlx": [
            "mlx-whisper",
        ],
        # NVIDIA GPU (Windows/Linux)
        "cuda": [
            "faster-whisper",
            "torch",
        ],
        # CPU fallback (any platform)
        "cpu": [
            "openai-whisper",
            "torch",
        ],
        # Enhanced Finnish lemmatization (macOS/Linux only)
        # Requires system library: brew install libvoikko (macOS) or apt install libvoikko-dev voikko-fi (Linux)
        "voikko": [
            "libvoikko",
        ],
    },
    entry_points={
        'console_scripts': [
            'transcribe=transcriber.main:main',
        ],
    },
)
