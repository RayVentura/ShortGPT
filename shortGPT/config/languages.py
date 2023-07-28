
from enum import Enum

class Language(Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    ARABIC = "Arabic"
    GERMAN = "German"
    POLISH = "Polish"
    ITALIAN = "Italian"
    PORTUGUESE = "Portuguese"
    AFRIKAANS = "Afrikaans"
    AMHARIC = "Amharic"
    AZERBAIJANI = "Azerbaijani"
    BULGARIAN = "Bulgarian"
    BENGALI = "Bengali"
    BOSNIAN = "Bosnian"
    CATALAN = "Catalan"
    CZECH = "Czech"
    WELSH = "Welsh"
    DANISH = "Danish"
    GREEK = "Greek"
    ESTONIAN = "Estonian"
    PERSIAN = "Persian"
    FINNISH = "Finnish"
    FILIPINO = "Filipino"
    GALICIAN = "Galician"
    GUJARATI = "Gujarati"
    HEBREW = "Hebrew"
    HINDI = "Hindi"
    CROATIAN = "Croatian"
    HUNGARIAN = "Hungarian"
    INDONESIAN = "Indonesian"
    ICELANDIC = "Icelandic"
    JAPANESE = "Japanese"
    JAVANESE = "Javanese"
    GEORGIAN = "Georgian"
    KAZAKH = "Kazakh"
    KHMER = "Khmer"
    KANNADA = "Kannada"
    KOREAN = "Korean"
    LAO = "Lao"
    LITHUANIAN = "Lithuanian"
    LATVIAN = "Latvian"
    MACEDONIAN = "Macedonian"
    MALAYALAM = "Malayalam"
    MONGOLIAN = "Mongolian"
    MARATHI = "Marathi"
    MALAY = "Malay"
    MALTESE = "Maltese"
    MYANMAR = "Myanmar"
    NORWEGIAN = "Norwegian"
    NEPALI = "Nepali"
    DUTCH = "Dutch"
    NORWEGIAN_BOKMAL = "Norwegian Bokmål"
    NORWEGIAN_NYNORSK = "Norwegian Nynorsk"
    PASHTO = "Pashto"
    ROMANIAN = "Romanian"
    RUSSIAN = "Russian"
    SINHALA = "Sinhala"
    SLOVAK = "Slovak"
    SLOVENIAN = "Slovenian"
    SOMALI = "Somali"
    ALBANIAN = "Albanian"
    SERBIAN = "Serbian"
    SUNDANESE = "Sundanese"
    SWEDISH = "Swedish"
    SWAHILI = "Swahili"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    THAI = "Thai"
    TURKISH = "Turkish"
    UKRAINIAN = "Ukrainian"
    URDU = "Urdu"
    UZBEK = "Uzbek"
    VIETNAMESE = "Vietnamese"
    CHINESE = "Chinese"
    ZULU = "Zulu"

ELEVEN_SUPPORTED_LANGUAGES=[Language.ENGLISH,
    Language.SPANISH,
    Language.FRENCH,
    Language.ARABIC,
    Language.GERMAN,
    Language.POLISH,
    Language.ITALIAN,
    Language.PORTUGUESE]

LANGUAGE_ACRONYM_MAPPING={
    Language.ENGLISH : "en",
    Language.SPANISH : "es",
    Language.FRENCH : "fr",
    Language.ARABIC : "ar",
    Language.GERMAN : "de",
    Language.POLISH : "pl",
    Language.ITALIAN : "it",
    Language.PORTUGUESE : "pt",
    Language.AFRIKAANS : "af",
    Language.AMHARIC : "am",
    Language.AZERBAIJANI : "az",
    Language.BULGARIAN : "bg",
    Language.BENGALI : "bn",
    Language.BOSNIAN : "bs",
    Language.CATALAN : "ca",
    Language.CZECH : "cs",
    Language.WELSH : "cy",
    Language.DANISH : "da",
    Language.GREEK : "el",
    Language.ESTONIAN : "et",
    Language.PERSIAN : "fa",
    Language.FINNISH : "fi",
    Language.FILIPINO : "fil",
    Language.GALICIAN : "gl",
    Language.GUJARATI : "gu",
    Language.HEBREW : "he",
    Language.HINDI : "hi",
    Language.CROATIAN : "hr",
    Language.HUNGARIAN : "hu",
    Language.INDONESIAN : "id",
    Language.ICELANDIC : "is",
    Language.JAPANESE : "ja",
    Language.JAVANESE : "jv",
    Language.GEORGIAN : "ka",
    Language.KAZAKH : "kk",
    Language.KHMER : "km",
    Language.KANNADA : "kn",
    Language.KOREAN : "ko",
    Language.LAO : "lo",
    Language.LITHUANIAN : "lt",
    Language.LATVIAN : "lv",
    Language.MACEDONIAN : "mk",
    Language.MALAYALAM : "ml",
    Language.MONGOLIAN : "mn",
    Language.MARATHI : "mr",
    Language.MALAY : "ms",
    Language.MALTESE : "mt",
    Language.MYANMAR : "my",
    Language.NORWEGIAN : "no",
    Language.NEPALI : "ne",
    Language.DUTCH : "nl",
    Language.NORWEGIAN_BOKMAL : "nb",
    Language.NORWEGIAN_NYNORSK : "nn",
    Language.PASHTO : "ps",
    Language.ROMANIAN : "ro",
    Language.RUSSIAN : "ru",
    Language.SINHALA : "si",
    Language.SLOVAK : "sk",
    Language.SLOVENIAN : "sl",
    Language.SOMALI : "so",
    Language.ALBANIAN : "sq",
    Language.SERBIAN : "sr",
    Language.SUNDANESE : "su",
    Language.SWEDISH : "sv",
    Language.SWAHILI : "sw",
    Language.TAMIL : "ta",
    Language.TELUGU : "te",
    Language.THAI : "th",
    Language.TURKISH : "tr",
    Language.UKRAINIAN : "uk",
    Language.URDU : "ur",
    Language.UZBEK : "uz",
    Language.VIETNAMESE : "vi",
    Language.CHINESE : "zh",
    Language.ZULU : "zu",
}
ACRONYM_LANGUAGE_MAPPING = {v: k for k, v in LANGUAGE_ACRONYM_MAPPING.items()}

EDGE_TTS_VOICENAME_MAPPING = {
    Language.ENGLISH: {'male': 'en-AU-WilliamNeural', 'female': 'en-AU-NatashaNeural'},
    Language.SPANISH: {'male': 'es-AR-TomasNeural', 'female': 'es-AR-ElenaNeural'},
    Language.FRENCH: {'male': 'fr-CA-AntoineNeural', 'female': 'fr-CA-SylvieNeural'},
    Language.ARABIC: {'male': 'ar-AE-HamdanNeural', 'female': 'ar-AE-FatimaNeural'},
    Language.GERMAN: {'male': 'de-DE-ConradNeural', 'female': 'de-DE-KatjaNeural'},
    Language.POLISH: {'male': 'pl-PL-MarekNeural', 'female': 'pl-PL-ZofiaNeural'},
    Language.ITALIAN: {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    Language.PORTUGUESE: {'male': 'pt-BR-AntonioNeural', 'female': 'pt-BR-FranciscaNeural'},
    Language.AFRIKAANS: {'male': 'af-ZA-WillemNeural', 'female': 'af-ZA-AdriNeural'},
    Language.AMHARIC: {'male': 'am-ET-AmehaNeural', 'female': 'am-ET-MekdesNeural'},
    Language.AZERBAIJANI: {'male': 'az-AZ-BabekNeural', 'female': 'az-AZ-BanuNeural'},
    Language.BULGARIAN: {'male': 'bg-BG-BorislavNeural', 'female': 'bg-BG-KalinaNeural'},
    Language.BENGALI: {'male': 'bn-BD-PradeepNeural', 'female': 'bn-BD-NabanitaNeural'},
    Language.BOSNIAN: {'male': 'bs-BA-GoranNeural', 'female': 'bs-BA-VesnaNeural'},
    Language.CATALAN: {'male': 'ca-ES-EnricNeural', 'female': 'ca-ES-JoanaNeural'},
    Language.CZECH: {'male': 'cs-CZ-AntoninNeural', 'female': 'cs-CZ-VlastaNeural'},
    Language.WELSH: {'male': 'cy-GB-AledNeural', 'female': 'cy-GB-NiaNeural'},
    Language.DANISH: {'male': 'da-DK-JeppeNeural', 'female': 'da-DK-ChristelNeural'},
    Language.GREEK: {'male': 'el-GR-NestorasNeural', 'female': 'el-GR-AthinaNeural'},
    Language.ESTONIAN: {'male': 'et-EE-KertNeural', 'female': 'et-EE-AnuNeural'},
    Language.PERSIAN: {'male': 'fa-IR-FaridNeural', 'female': 'fa-IR-DilaraNeural'},
    Language.FINNISH: {'male': 'fi-FI-HarriNeural', 'female': 'fi-FI-NooraNeural'},
    Language.FILIPINO: {'male': 'fil-PH-AngeloNeural', 'female': 'fil-PH-BlessicaNeural'},
    Language.GALICIAN: {'male': 'gl-ES-RoiNeural', 'female': 'gl-ES-SabelaNeural'},
    Language.GUJARATI: {'male': 'gu-IN-NiranjanNeural', 'female': 'gu-IN-DhwaniNeural'},
    Language.HEBREW: {'male': 'he-IL-AvriNeural', 'female': 'he-IL-HilaNeural'},
    Language.HINDI: {'male': 'hi-IN-MadhurNeural', 'female': 'hi-IN-SwaraNeural'},
    Language.CROATIAN: {'male': 'hr-HR-SreckoNeural', 'female': 'hr-HR-GabrijelaNeural'},
    Language.HUNGARIAN: {'male': 'hu-HU-TamasNeural', 'female': 'hu-HU-NoemiNeural'},
    Language.INDONESIAN: {'male': 'id-ID-ArdiNeural', 'female': 'id-ID-GadisNeural'},
    Language.ICELANDIC: {'male': 'is-IS-GunnarNeural', 'female': 'is-IS-GudrunNeural'},
    Language.ITALIAN: {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    Language.JAPANESE: {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},
    Language.JAVANESE: {'male': 'jv-ID-DimasNeural', 'female': 'jv-ID-SitiNeural'},
    Language.GEORGIAN: {'male': 'ka-GE-GiorgiNeural', 'female': 'ka-GE-EkaNeural'},
    Language.KAZAKH: {'male': 'kk-KZ-DauletNeural', 'female': 'kk-KZ-AigulNeural'},
    Language.KHMER: {'male': 'km-KH-PisethNeural', 'female': 'km-KH-SreymomNeural'},
    Language.KANNADA: {'male': 'kn-IN-GaganNeural', 'female': 'kn-IN-SapnaNeural'},
    Language.KOREAN: {'male': 'ko-KR-InJoonNeural', 'female': 'ko-KR-SunHiNeural'},
    Language.LAO: {'male': 'lo-LA-KeomanyNeural', 'female': 'lo-LA-ChanthavongNeural'},
    Language.LITHUANIAN: {'male': 'lt-LT-LeonasNeural', 'female': 'lt-LT-OnaNeural'},
    Language.LATVIAN: {'male': 'lv-LV-NilsNeural', 'female': 'lv-LV-EveritaNeural'},
    Language.MACEDONIAN: {'male': 'mk-MK-AleksandarNeural', 'female': 'mk-MK-MarijaNeural'},
    Language.MALAYALAM: {'male': 'ml-IN-MidhunNeural', 'female': 'ml-IN-MidhunNeural'},
    Language.MONGOLIAN: {'male': 'mn-MN-YesuiNeural', 'female': 'mn-MN-BataaNeural'},
    Language.MARATHI: {'male': 'mr-IN-ManoharNeural', 'female': 'mr-IN-AarohiNeural'},
    Language.MALAY: {'male': 'ms-MY-OsmanNeural', 'female': 'ms-MY-YasminNeural'},
    Language.MALTESE: {'male': 'mt-MT-JosephNeural', 'female': 'mt-MT-GraceNeural'},
    Language.MYANMAR: {'male': 'my-MM-ThihaNeural', 'female': 'my-MM-NilarNeural'},
    Language.NORWEGIAN: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    Language.NEPALI: {'male': 'ne-NP-SagarNeural', 'female': 'ne-NP-HemkalaNeural'},
    Language.DUTCH: {'male': 'nl-NL-MaartenNeural', 'female': 'nl-NL-FennaNeural'},
    Language.NORWEGIAN_BOKMAL: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    Language.NORWEGIAN_NYNORSK: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    Language.PASHTO: {'male': 'ps-AF-LatifaNeural', 'female': 'ps-AF-GulNawazNeural'},
    Language.ROMANIAN: {'male': 'ro-RO-EmilNeural', 'female': 'ro-RO-AlinaNeural'},
    Language.RUSSIAN: {'male': 'ru-RU-DmitryNeural', 'female': 'ru-RU-SvetlanaNeural'},
    Language.SINHALA: {'male': 'si-LK-SameeraNeural', 'female': 'si-LK-ThiliniNeural'},
    Language.SLOVAK: {'male': 'sk-SK-LukasNeural', 'female': 'sk-SK-ViktoriaNeural'},
    Language.SLOVENIAN: {'male': 'sl-SI-RokNeural', 'female': 'sl-SI-PetraNeural'},
    Language.SOMALI: {'male': 'so-SO-MuuseNeural', 'female': 'so-SO-UbaxNeural'},
    Language.ALBANIAN: {'male': 'sq-AL-IlirNeural', 'female': 'sq-AL-AnilaNeural'},
    Language.SERBIAN: {'male': 'sr-RS-NicholasNeural', 'female': 'sr-RS-SophieNeural'},
    Language.SUNDANESE: {'male': 'su-ID-JajangNeural', 'female': 'su-ID-TutiNeural'},
    Language.SWEDISH: {'male': 'sv-SE-MattiasNeural', 'female': 'sv-SE-SofieNeural'},
    Language.SWAHILI: {'male': 'sw-TZ-DaudiNeural', 'female': 'sw-TZ-DaudiNeural'},
    Language.TAMIL: {'male': 'ta-IN-ValluvarNeural', 'female': 'ta-IN-PallaviNeural'},
    Language.TELUGU: {'male': 'te-IN-MohanNeural', 'female': 'te-IN-ShrutiNeural'},
    Language.THAI: {'male': 'th-TH-NiwatNeural', 'female': 'th-TH-PremwadeeNeural'},
    Language.TURKISH: {'male': 'tr-TR-AhmetNeural', 'female': 'tr-TR-EmelNeural'},
    Language.UKRAINIAN: {'male': 'uk-UA-OstapNeural', 'female': 'uk-UA-PolinaNeural'},
    Language.URDU: {'male': 'ur-PK-AsadNeural', 'female': 'ur-PK-UzmaNeural'},
    Language.UZBEK: {'male': 'uz-UZ-SardorNeural', 'female': 'uz-UZ-MadinaNeural'},
    Language.VIETNAMESE: {'male': 'vi-VN-NamMinhNeural', 'female': 'vi-VN-HoaiMyNeural'},
    Language.CHINESE: {'male': 'zh-CN-YunxiNeural', 'female': 'zh-CN-XiaoxiaoNeural'},
    Language.ZULU: {'male': 'zu-ZA-ThembaNeural', 'female': 'zu-ZA-ThandoNeural'}
}