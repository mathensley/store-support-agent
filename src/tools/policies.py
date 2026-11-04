import re
from functools import lru_cache
from typing import Literal

from langchain.tools import tool
from pypdf import PdfReader

from src.tools._csv import DATA_DIR


PolicyTopic = Literal[
    "loja",
    "horarios",
    "pagamento",
    "trocas_devolucoes",
    "frete_entregas",
    "promocoes",
    "atendimento",
    "garantia",
    "privacidade",
    "disposicoes_finais",
]

_PDF_PATH = DATA_DIR / "politicas_da_loja.pdf"
_SECTIONS = (
    ("loja", "1. Sobre a Empório da Música"),
    ("horarios", "2. Horário de Funcionamento"),
    ("pagamento", "3. Formas de Pagamento"),
    ("trocas_devolucoes", "4. Política de Trocas e Devoluções"),
    ("frete_entregas", "5. Política de Frete e Entregas"),
    ("promocoes", "6. Promoções e Descontos"),
    ("atendimento", "7. Atendimento via WhatsApp"),
    ("garantia", "8. Garantia"),
    ("privacidade", "9. Privacidade e Proteção de Dados"),
    ("disposicoes_finais", "10. Disposições Finais"),
)

def _page_text(page) -> str:
    text = " ".join((page.extract_text() or "").split())
    text = re.sub(r"^Empório da Música Manual de Políticas e Procedimentos\s*", "", text)
    
    return re.sub(r"\s+Página \d+$", "", text)

@lru_cache(maxsize=1)
def _load_sections() -> dict[str, dict]:
    """Extrai as seções uma vez por processo, preservando as páginas do PDF."""

    reader = PdfReader(_PDF_PATH)
    document = ""
    page_spans = []
    for page_number, page in enumerate(reader.pages, start=1):
        if page_number == 1:  # Capa; o endereço também consta na seção 1.
            continue
        start = len(document)
        document += _page_text(page) + "\n"
        page_spans.append((page_number, start, len(document)))

    starts = []
    for topic, title in _SECTIONS:
        position = document.find(title)
        if position < 0:
            raise ValueError(f"Seção não encontrada no PDF: {title}")
        starts.append((topic, title, position))
    if [position for _, _, position in starts] != sorted(position for _, _, position in starts):
        raise ValueError("As seções do PDF estão fora da ordem esperada.")

    sections = {}
    for index, (topic, title, start) in enumerate(starts):
        end = starts[index + 1][2] if index + 1 < len(starts) else len(document)
        pages = [
            number for number, page_start, page_end in page_spans
            if page_start < end and page_end > start
        ]
        sections[topic] = {
            "section": title,
            "pages": pages,
            "text": document[start:end].strip()
        }
    return sections


@tool
def consultar_politicas(topico: PolicyTopic) -> dict:
    """Consulte uma seção do PDF de políticas e obtenha texto com página de origem.

    Escolha `loja` para endereço, contato e escopo; `horarios` para funcionamento;
    `pagamento` para PIX, boleto e parcelamento; `trocas_devolucoes` para arrependimento, troca e defeito;
    `frete_entregas` para entrega e rastreio; `promocoes` para regras de descontos;
    `atendimento` para WhatsApp e conduta; `garantia` para cobertura;
    `privacidade` para dados pessoais; `disposicoes_finais` para dúvidas ou atualização do manual.

    Consulte mais de um tópico se a pergunta combinar políticas diferentes.
    """

    return {
        "topic": topico,
        **_load_sections()[topico],
        "source": "data/politicas_da_loja.pdf"
    }