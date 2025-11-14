import pytest
from src.detector import luhn_check, identify_brand


def test_luhn_valid_examples():
    # Números de exemplo válidos para Luhn
    assert luhn_check("4111111111111111")  # Visa
    assert luhn_check("5555555555554444")  # MasterCard
    assert luhn_check("378282246310005")   # Amex
    assert luhn_check("6011111111111117")  # Discover


def test_identify_visa():
    assert identify_brand("4111111111111111") == "Visa"
    assert identify_brand("4012888888881881") == "Visa"


def test_identify_mastercard():
    assert identify_brand("5555555555554444") == "MasterCard"
    # Faixa 2221–2720
    assert identify_brand("2221000000000009") == "MasterCard"
    assert identify_brand("2720990000000002") == "MasterCard"


def test_identify_amex():
    assert identify_brand("378282246310005") == "American Express"
    assert identify_brand("371449635398431") == "American Express"


def test_identify_discover():
    assert identify_brand("6011111111111117") == "Discover"
    assert identify_brand("6011000990139424") == "Discover"


def test_non_numeric_or_invalid():
    assert identify_brand("4111 1111 1111 1111") == "Visa"   # espaços ignorados
    assert identify_brand("4111-1111-1111-1111") is None     # traços não permitidos (apenas dígitos/espacos)
    assert identify_brand("abcd") is None
    # Luhn inválido
    assert identify_brand("4111111111111112") is None


def test_lengths_and_unknown():
    # Comprimento incorreto para Amex
    assert identify_brand("34111111111111111") is None
    # Prefixo desconhecido
    assert identify_brand("1234567890123456") is None
