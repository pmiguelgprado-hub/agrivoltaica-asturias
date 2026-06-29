"""Guards de honestidad del marco legal: toda cifra/afirmación citada EN FUENTE."""
from app.core.legal import MARCO_LEGAL, ESTADOS, DOMINIOS_OFICIALES


def test_toda_entrada_tiene_fuente_https():
    for item in MARCO_LEGAL:
        assert item.fuente_url.startswith("https://"), item.tema
        assert item.fuente_label.strip(), item.tema
        assert item.norma.strip(), item.tema


def test_fuentes_son_oficiales():
    # Disciplina del proyecto: BOE / administración, no blogs ni memoria.
    for item in MARCO_LEGAL:
        assert any(d in item.fuente_url for d in DOMINIOS_OFICIALES), item.fuente_url


def test_estados_validos():
    for item in MARCO_LEGAL:
        assert item.estado in ESTADOS, (item.tema, item.estado)


def test_caveat_agrivoltaico_visible():
    # La incertidumbre de los criterios técnicos PAC debe estar presente y etiquetada.
    assert any(i.estado == "por_concretar" for i in MARCO_LEGAL)
