"""Configuration constants and language definitions."""

import logging

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(message)s'

# Supported File Extensions
EXTENSIONS = {
    'audio': {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.aac'},
    'video': {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.wmv', '.flv'},
    'text': {'.srt', '.vtt', '.pdf', '.docx', '.html', '.htm'}
}

# Language Definitions
LANGUAGES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German',
    'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
    'eu': 'Basque', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
    'ga': 'Irish', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian',
    'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian',
    'mk': 'Macedonian', 'ms': 'Malay', 'nb': 'Norwegian Bokmål', 'nl': 'Dutch',
    'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
    'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sq': 'Albanian',
    'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Tagalog',
    'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
    'zh': 'Chinese',
}

LANG_ALIASES = {'no': 'nb'}

# Spacy Model Mappings
SPACY_MODELS = {
    'ca': 'ca_core_news_sm', 'da': 'da_core_news_sm', 'de': 'de_core_news_sm',
    'el': 'el_core_news_sm', 'en': 'en_core_web_sm', 'es': 'es_core_news_sm',
    'fi': 'fi_core_news_sm', 'fr': 'fr_core_news_sm', 'hr': 'hr_core_news_sm',
    'it': 'it_core_news_sm', 'ja': 'ja_core_news_sm', 'ko': 'ko_core_news_sm',
    'lt': 'lt_core_news_sm', 'mk': 'mk_core_news_sm', 'nb': 'nb_core_news_sm',
    'nl': 'nl_core_news_sm', 'pl': 'pl_core_news_sm', 'pt': 'pt_core_news_sm',
    'ro': 'ro_core_news_sm', 'ru': 'ru_core_news_sm', 'sl': 'sl_core_news_sm',
    'sv': 'sv_core_news_sm', 'uk': 'uk_core_news_sm', 'zh': 'zh_core_web_sm',
}
