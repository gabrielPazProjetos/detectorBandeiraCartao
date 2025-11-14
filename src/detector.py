from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass(frozen=True)
class BrandRule:
    name: str
    iin_ranges: List[Tuple[int, int]]  # Lista de faixas IIN/BIN (prefixos numéricos)
    lengths: List[int]                 # Comprimentos do PAN aceitos (número completo do cartão)


def luhn_check(card_number: str) -> bool:
    """
    Valida o número do cartão usando o algoritmo de Luhn.
    - Remove espaços
    - Verifica se é numérico
    - Aplica Luhn e retorna True/False
    """
    digits = card_number.replace(" ", "")
    if not digits.isdigit():
        return False

    total = 0
    reverse = digits[::-1]
    for i, ch in enumerate(reverse):
        n = int(ch)
        if i % 2 == 1:  # dobra dígitos em posições ímpares no reverso (equivale à regra do Luhn)
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def _starts_in_range(digits: str, start: int, end: int) -> bool:
    """
    Verifica se os dígitos iniciais (mesma quantidade de dígitos do 'end') estão dentro da faixa [start, end].
    """
    width = len(str(end))
    prefix = digits[:width]
    if not prefix.isdigit():
        return False
    val = int(prefix)
    return start <= val <= end


def _matches_any_range(digits: str, ranges: List[Tuple[int, int]]) -> bool:
    return any(_starts_in_range(digits, start, end) for start, end in ranges)


# Regras de identificação de bandeiras (conjuntas e razoavelmente abrangentes)
BRAND_RULES: List[BrandRule] = [
    # Visa: prefixo 4, geralmente 13, 16 ou 19 dígitos
    BrandRule(name="Visa", iin_ranges=[(4, 4)], lengths=[13, 16, 19]),

    # MasterCard: 51–55 e 2221–2720 (16 dígitos)
    BrandRule(name="MasterCard", iin_ranges=[(51, 55), (2221, 2720)], lengths=[16]),

    # American Express: 34, 37 (15 dígitos)
    BrandRule(name="American Express", iin_ranges=[(34, 34), (37, 37)], lengths=[15]),

    # Discover (simplificado): 6011, 65, 644–649 (16 ou 19)
    BrandRule(name="Discover", iin_ranges=[(6011, 6011), (65, 65), (644, 649)], lengths=[16, 19]),

    # Diners Club (faixas comuns): 300–305, 36, 38–39 (14 ou 16)
    BrandRule(name="Diners Club", iin_ranges=[(300, 305), (36, 36), (38, 39)], lengths=[14, 16]),

    # JCB: 3528–3589 (16 a 19 dígitos)
    BrandRule(name="JCB", iin_ranges=[(3528, 3589)], lengths=[16, 17, 18, 19]),

    # Elo (faixas conhecidas comuns — podem variar entre emissores)
    BrandRule(
        name="Elo",
        iin_ranges=[
            (401178, 401179), (431274, 431274), (438935, 438935), (451416, 451416),
            (457393, 457393), (457631, 457632), (504175, 504175), (506699, 506778),
            (509000, 509999), (627780, 627780), (636297, 636297), (636368, 636368)
        ],
        lengths=[16]
    ),

    # Hipercard (típico: 6062)
    BrandRule(name="Hipercard", iin_ranges=[(6062, 6062)], lengths=[16, 19]),

    # Aura (típico: 50)
    BrandRule(name="Aura", iin_ranges=[(50, 50)], lengths=[16, 19]),
]


def identify_brand(card_number: str, validate_luhn: bool = True) -> Optional[str]:
    """
    Retorna o nome da bandeira com base em prefixos (IIN/BIN) e comprimento.
    Opcionalmente aplica o Luhn. Se não corresponder, retorna None.
    """
    digits = card_number.replace(" ", "")
    if not digits.isdigit():
        return None

    length = len(digits)

    for rule in BRAND_RULES:
        if length in rule.lengths and _matches_any_range(digits, rule.iin_ranges):
            if validate_luhn:
                return rule.name if luhn_check(digits) else None
            return rule.name

    return None


def identify_with_details(card_number: str, validate_luhn: bool = True) -> dict:
    """
    Retorna um dict com detalhes: bandeira, válido_luhn, comprimento e prefixo avaliado.
    Útil para logs, debug e exibição em UI/CLI.
    """
    digits = card_number.replace(" ", "")
    brand = identify_brand(digits, validate_luhn=validate_luhn)
    luhn_valid = luhn_check(digits) if validate_luhn else None

    # prefixo de até 6 dígitos (IIN clássico)
    prefix_6 = digits[:6] if len(digits) >= 6 else digits

    return {
        "brand": brand,
        "length": len(digits),
        "iin_prefix": prefix_6,
        "luhn_valid": luhn_valid,
    }
