"""
GoLingu - Language Models
Supported languages registry and helpers.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Language:
    code: str          # BCP-47 code
    name: str          # English name
    nativeName: str    # Name in that language


# Comprehensive list of supported languages (BCP-47 codes)
SUPPORTED_LANGUAGES: Dict[str, Language] = {
    "af": Language("af", "Afrikaans", "Afrikaans"),
    "sq": Language("sq", "Albanian", "Shqip"),
    "am": Language("am", "Amharic", "አማርኛ"),
    "ar": Language("ar", "Arabic", "العربية"),
    "hy": Language("hy", "Armenian", "Հայերեն"),
    "az": Language("az", "Azerbaijani", "Azərbaycan"),
    "eu": Language("eu", "Basque", "Euskara"),
    "be": Language("be", "Belarusian", "Беларуская"),
    "bn": Language("bn", "Bengali", "বাংলা"),
    "bs": Language("bs", "Bosnian", "Bosanski"),
    "bg": Language("bg", "Bulgarian", "Български"),
    "ca": Language("ca", "Catalan", "Català"),
    "zh": Language("zh", "Chinese (Simplified)", "中文"),
    "zh-tw": Language("zh-tw", "Chinese (Traditional)", "繁體中文"),
    "hr": Language("hr", "Croatian", "Hrvatski"),
    "cs": Language("cs", "Czech", "Čeština"),
    "da": Language("da", "Danish", "Dansk"),
    "nl": Language("nl", "Dutch", "Nederlands"),
    "en": Language("en", "English", "English"),
    "eo": Language("eo", "Esperanto", "Esperanto"),
    "et": Language("et", "Estonian", "Eesti"),
    "fi": Language("fi", "Finnish", "Suomi"),
    "fr": Language("fr", "French", "Français"),
    "gl": Language("gl", "Galician", "Galego"),
    "ka": Language("ka", "Georgian", "ქართული"),
    "de": Language("de", "German", "Deutsch"),
    "el": Language("el", "Greek", "Ελληνικά"),
    "gu": Language("gu", "Gujarati", "ગુજરાતી"),
    "ht": Language("ht", "Haitian Creole", "Kreyòl ayisyen"),
    "ha": Language("ha", "Hausa", "Hausa"),
    "he": Language("he", "Hebrew", "עברית"),
    "hi": Language("hi", "Hindi", "हिन्दी"),
    "hu": Language("hu", "Hungarian", "Magyar"),
    "is": Language("is", "Icelandic", "Íslenska"),
    "ig": Language("ig", "Igbo", "Igbo"),
    "id": Language("id", "Indonesian", "Bahasa Indonesia"),
    "ga": Language("ga", "Irish", "Gaeilge"),
    "it": Language("it", "Italian", "Italiano"),
    "ja": Language("ja", "Japanese", "日本語"),
    "kn": Language("kn", "Kannada", "ಕನ್ನಡ"),
    "kk": Language("kk", "Kazakh", "Қазақша"),
    "km": Language("km", "Khmer", "ខ្មែរ"),
    "ko": Language("ko", "Korean", "한국어"),
    "ku": Language("ku", "Kurdish", "Kurdî"),
    "ky": Language("ky", "Kyrgyz", "Кыргызча"),
    "lo": Language("lo", "Lao", "ລາວ"),
    "lv": Language("lv", "Latvian", "Latviešu"),
    "lt": Language("lt", "Lithuanian", "Lietuvių"),
    "lb": Language("lb", "Luxembourgish", "Lëtzebuergesch"),
    "mk": Language("mk", "Macedonian", "Македонски"),
    "mg": Language("mg", "Malagasy", "Malagasy"),
    "ms": Language("ms", "Malay", "Bahasa Melayu"),
    "ml": Language("ml", "Malayalam", "മലയാളം"),
    "mt": Language("mt", "Maltese", "Malti"),
    "mi": Language("mi", "Maori", "Māori"),
    "mr": Language("mr", "Marathi", "मराठी"),
    "mn": Language("mn", "Mongolian", "Монгол"),
    "my": Language("my", "Myanmar (Burmese)", "မြန်မာဘာသာ"),
    "ne": Language("ne", "Nepali", "नेपाली"),
    "no": Language("no", "Norwegian", "Norsk"),
    "or": Language("or", "Odia (Oriya)", "ଓଡ଼ିଆ"),
    "ps": Language("ps", "Pashto", "پښتو"),
    "fa": Language("fa", "Persian", "فارسی"),
    "pl": Language("pl", "Polish", "Polski"),
    "pt": Language("pt", "Portuguese", "Português"),
    "pa": Language("pa", "Punjabi", "ਪੰਜਾਬੀ"),
    "ro": Language("ro", "Romanian", "Română"),
    "ru": Language("ru", "Russian", "Русский"),
    "sm": Language("sm", "Samoan", "Samoan"),
    "gd": Language("gd", "Scots Gaelic", "Gàidhlig"),
    "sr": Language("sr", "Serbian", "Српски"),
    "st": Language("st", "Sesotho", "Sesotho"),
    "sn": Language("sn", "Shona", "Shona"),
    "sd": Language("sd", "Sindhi", "سنڌي"),
    "si": Language("si", "Sinhala", "සිංහල"),
    "sk": Language("sk", "Slovak", "Slovenčina"),
    "sl": Language("sl", "Slovenian", "Slovenščina"),
    "so": Language("so", "Somali", "Soomaali"),
    "es": Language("es", "Spanish", "Español"),
    "su": Language("su", "Sundanese", "Sunda"),
    "sw": Language("sw", "Swahili", "Kiswahili"),
    "sv": Language("sv", "Swedish", "Svenska"),
    "tg": Language("tg", "Tajik", "Тоҷикӣ"),
    "ta": Language("ta", "Tamil", "தமிழ்"),
    "tt": Language("tt", "Tatar", "Татарча"),
    "te": Language("te", "Telugu", "తెలుగు"),
    "th": Language("th", "Thai", "ภาษาไทย"),
    "tr": Language("tr", "Turkish", "Türkçe"),
    "tk": Language("tk", "Turkmen", "Türkmençe"),
    "uk": Language("uk", "Ukrainian", "Українська"),
    "ur": Language("ur", "Urdu", "اردو"),
    "ug": Language("ug", "Uyghur", "ئۇيغۇرچە"),
    "uz": Language("uz", "Uzbek", "O'zbek"),
    "vi": Language("vi", "Vietnamese", "Tiếng Việt"),
    "cy": Language("cy", "Welsh", "Cymraeg"),
    "xh": Language("xh", "Xhosa", "isiXhosa"),
    "yi": Language("yi", "Yiddish", "ייִדיש"),
    "yo": Language("yo", "Yoruba", "Yorùbá"),
    "zu": Language("zu", "Zulu", "isiZulu"),
}


def is_supported_language(code: str) -> bool:
    return code.lower() in SUPPORTED_LANGUAGES


def get_language(code: str) -> Optional[Language]:
    return SUPPORTED_LANGUAGES.get(code.lower())
