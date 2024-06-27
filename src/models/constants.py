from collections import namedtuple


# Named tuple to store the language and the corresponding model
Language = namedtuple("Language", ["code", "name", "greeting"])

LANGUAGE_MAPPING = {
    "en": Language("en", "English", "Hello"),
    "es": Language("es", "Spanish", "Hola"),
    "es-MX": Language("es-MX", "Mexican Spanish", "Hola"),
    "fr": Language("fr", "French", "Bonjour"),
    "de": Language("de", "German", "Hallo"),
    "de-ch": Language("de-ch", "Swiss German", "Hallo"),
    "it": Language("it", "Italian", "Ciao"),
    "tr": Language("tr", "Turkish", "Merhaba"),
    "pt-BR": Language("pt-BR", "Brazilian Portuguese", "Olá"),
    "jp": Language("jp", "Japanese", "こんにちは"),
    "ar": Language("ar", "Arabic", "مرحبا"),
}
