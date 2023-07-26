
from enum import Enum

class EdgeTTSLanguage(Enum):
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
    PANJABI = "Panjabi"
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
language_to_voice_name = {
    EdgeTTSLanguage.ENGLISH: {'male': 'en-AU-WilliamNeural', 'female': 'en-AU-NatashaNeural'},
    EdgeTTSLanguage.SPANISH: {'male': 'es-AR-TomasNeural', 'female': 'es-AR-ElenaNeural'},
    EdgeTTSLanguage.FRENCH: {'male': 'fr-CA-AntoineNeural', 'female': 'fr-CA-SylvieNeural'},
    EdgeTTSLanguage.ARABIC: {'male': 'ar-AE-HamdanNeural', 'female': 'ar-AE-FatimaNeural'},
    EdgeTTSLanguage.GERMAN: {'male': 'de-DE-ConradNeural', 'female': 'de-DE-KatjaNeural'},
    EdgeTTSLanguage.POLISH: {'male': 'pl-PL-MarekNeural', 'female': 'pl-PL-ZofiaNeural'},
    EdgeTTSLanguage.ITALIAN: {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    EdgeTTSLanguage.PORTUGUESE: {'male': 'pt-BR-AntonioNeural', 'female': 'pt-BR-FranciscaNeural'},
    EdgeTTSLanguage.AFRIKAANS: {'male': 'af-ZA-WillemNeural', 'female': 'af-ZA-AdriNeural'},
    EdgeTTSLanguage.AMHARIC: {'male': 'am-ET-AmehaNeural', 'female': 'am-ET-MekdesNeural'},
    EdgeTTSLanguage.AZERBAIJANI: {'male': 'az-AZ-BabekNeural', 'female': 'az-AZ-BanuNeural'},
    EdgeTTSLanguage.BULGARIAN: {'male': 'bg-BG-BorislavNeural', 'female': 'bg-BG-KalinaNeural'},
    EdgeTTSLanguage.BENGALI: {'male': 'bn-BD-PradeepNeural', 'female': 'bn-BD-NabanitaNeural'},
    EdgeTTSLanguage.BOSNIAN: {'male': 'bs-BA-GoranNeural', 'female': 'bs-BA-VesnaNeural'},
    EdgeTTSLanguage.CATALAN: {'male': 'ca-ES-EnricNeural', 'female': 'ca-ES-JoanaNeural'},
    EdgeTTSLanguage.CZECH: {'male': 'cs-CZ-AntoninNeural', 'female': 'cs-CZ-VlastaNeural'},
    EdgeTTSLanguage.WELSH: {'male': 'cy-GB-AledNeural', 'female': 'cy-GB-NiaNeural'},
    EdgeTTSLanguage.DANISH: {'male': 'da-DK-JeppeNeural', 'female': 'da-DK-ChristelNeural'},
    EdgeTTSLanguage.GREEK: {'male': 'el-GR-NestorasNeural', 'female': 'el-GR-AthinaNeural'},
    EdgeTTSLanguage.ESTONIAN: {'male': 'et-EE-KertNeural', 'female': 'et-EE-AnuNeural'},
    EdgeTTSLanguage.PERSIAN: {'male': 'fa-IR-FaridNeural', 'female': 'fa-IR-DilaraNeural'},
    EdgeTTSLanguage.FINNISH: {'male': 'fi-FI-HarriNeural', 'female': 'fi-FI-NooraNeural'},
    EdgeTTSLanguage.FILIPINO: {'male': 'fil-PH-AngeloNeural', 'female': 'fil-PH-BlessicaNeural'},
    EdgeTTSLanguage.GALICIAN: {'male': 'gl-ES-RoiNeural', 'female': 'gl-ES-SabelaNeural'},
    EdgeTTSLanguage.GUJARATI: {'male': 'gu-IN-NiranjanNeural', 'female': 'gu-IN-DhwaniNeural'},
    EdgeTTSLanguage.HEBREW: {'male': 'he-IL-AvriNeural', 'female': 'he-IL-HilaNeural'},
    EdgeTTSLanguage.HINDI: {'male': 'hi-IN-PrabhatNeural', 'female': 'hi-IN-SwaraNeural'},
    EdgeTTSLanguage.CROATIAN: {'male': 'hr-HR-SreckoNeural', 'female': 'hr-HR-GabrijelaNeural'},
    EdgeTTSLanguage.HUNGARIAN: {'male': 'hu-HU-TamasNeural', 'female': 'hu-HU-NoemiNeural'},
    EdgeTTSLanguage.INDONESIAN: {'male': 'id-ID-ArdiNeural', 'female': 'id-ID-GadisNeural'},
    EdgeTTSLanguage.ICELANDIC: {'male': 'is-IS-GunnarNeural', 'female': 'is-IS-GudrunNeural'},
    EdgeTTSLanguage.ITALIAN: {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    EdgeTTSLanguage.JAPANESE: {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},
    EdgeTTSLanguage.JAVANESE: {'male': 'jv-ID-DimasNeural', 'female': 'jv-ID-SitiNeural'},
    EdgeTTSLanguage.GEORGIAN: {'male': 'ka-GE-GiorgiNeural', 'female': 'ka-GE-EkaNeural'},
    EdgeTTSLanguage.KAZAKH: {'male': 'kk-KZ-DauletNeural', 'female': 'kk-KZ-AigulNeural'},
    EdgeTTSLanguage.KHMER: {'male': 'km-KH-PisethNeural', 'female': 'km-KH-SreymomNeural'},
    EdgeTTSLanguage.KANNADA: {'male': 'kn-IN-GaganNeural', 'female': 'kn-IN-SapnaNeural'},
    EdgeTTSLanguage.KOREAN: {'male': 'ko-KR-InJoonNeural', 'female': 'ko-KR-SunHiNeural'},
    EdgeTTSLanguage.LAO: {'male': 'lo-LA-KeomanyNeural', 'female': 'lo-LA-ChanthavongNeural'},
    EdgeTTSLanguage.LITHUANIAN: {'male': 'lt-LT-LeonasNeural', 'female': 'lt-LT-OnaNeural'},
    EdgeTTSLanguage.LATVIAN: {'male': 'lv-LV-NilsNeural', 'female': 'lv-LV-EveritaNeural'},
    EdgeTTSLanguage.MACEDONIAN: {'male': 'mk-MK-AleksandarNeural', 'female': 'mk-MK-MarijaNeural'},
    EdgeTTSLanguage.MALAYALAM: {'male': 'ml-IN-ManoharNeural', 'female': 'ml-IN-MidhunNeural'},
    EdgeTTSLanguage.MONGOLIAN: {'male': 'mn-MN-YesuiNeural', 'female': 'mn-MN-BataaNeural'},
    EdgeTTSLanguage.MARATHI: {'male': 'mr-IN-ManoharNeural', 'female': 'mr-IN-AarohiNeural'},
    EdgeTTSLanguage.MALAY: {'male': 'ms-MY-OsmanNeural', 'female': 'ms-MY-YasminNeural'},
    EdgeTTSLanguage.MALTESE: {'male': 'mt-MT-JosephNeural', 'female': 'mt-MT-GraceNeural'},
    EdgeTTSLanguage.MYANMAR: {'male': 'my-MM-ThihaNeural', 'female': 'my-MM-NilarNeural'},
    EdgeTTSLanguage.NORWEGIAN: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    EdgeTTSLanguage.NEPALI: {'male': 'ne-NP-SagarNeural', 'female': 'ne-NP-HemkalaNeural'},
    EdgeTTSLanguage.DUTCH: {'male': 'nl-NL-MaartenNeural', 'female': 'nl-NL-FennaNeural'},
    EdgeTTSLanguage.NORWEGIAN_BOKMAL: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    EdgeTTSLanguage.NORWEGIAN_NYNORSK: {'male': 'nb-NO-FinnNeural', 'female': 'nb-NO-PernilleNeural'},
    EdgeTTSLanguage.PANJABI: {'male': 'pa-IN-GurdeepNeural', 'female': 'pa-IN-AmanNeural'},
    EdgeTTSLanguage.PASHTO: {'male': 'ps-AF-LatifaNeural', 'female': 'ps-AF-GulNawazNeural'},
    EdgeTTSLanguage.ROMANIAN: {'male': 'ro-RO-EmilNeural', 'female': 'ro-RO-AlinaNeural'},
    EdgeTTSLanguage.RUSSIAN: {'male': 'ru-RU-DmitryNeural', 'female': 'ru-RU-SvetlanaNeural'},
    EdgeTTSLanguage.SINHALA: {'male': 'si-LK-SameeraNeural', 'female': 'si-LK-ThiliniNeural'},
    EdgeTTSLanguage.SLOVAK: {'male': 'sk-SK-LukasNeural', 'female': 'sk-SK-ViktoriaNeural'},
    EdgeTTSLanguage.SLOVENIAN: {'male': 'sl-SI-RokNeural', 'female': 'sl-SI-PetraNeural'},
    EdgeTTSLanguage.SOMALI: {'male': 'so-SO-MuuseNeural', 'female': 'so-SO-UbaxNeural'},
    EdgeTTSLanguage.ALBANIAN: {'male': 'sq-AL-IlirNeural', 'female': 'sq-AL-AnilaNeural'},
    EdgeTTSLanguage.SERBIAN: {'male': 'sr-RS-NicholasNeural', 'female': 'sr-RS-SophieNeural'},
    EdgeTTSLanguage.SUNDANESE: {'male': 'su-ID-JajangNeural', 'female': 'su-ID-TutiNeural'},
    EdgeTTSLanguage.SWEDISH: {'male': 'sv-SE-MattiasNeural', 'female': 'sv-SE-SofieNeural'},
    EdgeTTSLanguage.SWAHILI: {'male': 'sw-TZ-ElimuNeural', 'female': 'sw-TZ-ImaniNeural'},
    EdgeTTSLanguage.TAMIL: {'male': 'ta-IN-ValluvarNeural', 'female': 'ta-IN-PallaviNeural'},
    EdgeTTSLanguage.TELUGU: {'male': 'te-IN-MohanNeural', 'female': 'te-IN-ShrutiNeural'},
    EdgeTTSLanguage.THAI: {'male': 'th-TH-NiwatNeural', 'female': 'th-TH-PremwadeeNeural'},
    EdgeTTSLanguage.TURKISH: {'male': 'tr-TR-AhmetNeural', 'female': 'tr-TR-EmelNeural'},
    EdgeTTSLanguage.UKRAINIAN: {'male': 'uk-UA-OstapNeural', 'female': 'uk-UA-PolinaNeural'},
    EdgeTTSLanguage.URDU: {'male': 'ur-PK-AsadNeural', 'female': 'ur-PK-UzmaNeural'},
    EdgeTTSLanguage.UZBEK: {'male': 'uz-UZ-SardorNeural', 'female': 'uz-UZ-MadinaNeural'},
    EdgeTTSLanguage.VIETNAMESE: {'male': 'vi-VN-NamMinhNeural', 'female': 'vi-VN-HoaiMyNeural'},
    EdgeTTSLanguage.CHINESE: {'male': 'zh-CN-YunxiNeural', 'female': 'zh-CN-XiaoxiaoNeural'},
    EdgeTTSLanguage.ZULU: {'male': 'zu-ZA-ThembaNeural', 'female': 'zu-ZA-ThandoNeural'}
}