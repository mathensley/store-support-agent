import re
import unicodedata


_IRREGULAR = {
    "violoes": "violao",
    "metais": "metal",
    "comecando": "iniciante",
    "comecar": "iniciante",
    "estudante": "iniciante",
    "estudantes": "iniciante",
    "estudo": "iniciante",
}
_STOPWORDS = {
    "a", "as", "ate", "com", "da", "de", "do", "em", "e", "o", "os",
    "para", "por", "qual", "quai", "que", "um", "uma", "opcao", "opcoe", "quero",
    "busco", "custa", "custando", "preco", "real", "reai", "disponivel",
    "disponivei", "instrumento",
}


def normalized(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    unaccented = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", unaccented))

def tokens(value: str, *, search_query: bool = False) -> set[str]:
    result = set()
    for token in normalized(value).split():
        token = _IRREGULAR.get(token, token)
        if token.endswith("s") and len(token) > 3:
            token = token[:-1]
        if not search_query or token not in _STOPWORDS:
            result.add(token)
    return result