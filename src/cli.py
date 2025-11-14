import sys
from detector import identify_with_details

BANNER = "Credit Card Detector (CLI) — Identifique bandeiras rapidamente"


def normalize_input(raw: str) -> str:
    return raw.strip()


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if argv and argv[0] in {"-h", "--help"}:
        print(BANNER)
        print("Uso:")
        print("  ccdetect <numero_do_cartao>")
        print("  ccdetect             # modo interativo")
        return 0

    if argv:
        number = normalize_input(argv[0])
        details = identify_with_details(number, validate_luhn=True)
        _print_result(number, details)
        return 0

    # Modo interativo
    print(BANNER)
    print("Digite o número do cartão (sem espaços ou com espaços; eles serão ignorados).")
    try:
        while True:
            raw = input("> ")
            number = normalize_input(raw)
            if not number:
                print("Encerrando.")
                break
            details = identify_with_details(number, validate_luhn=True)
            _print_result(number, details)
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrando.")
    return 0


def _print_result(number: str, details: dict) -> None:
    brand = details["brand"]
    luhn_ok = details["luhn_valid"]
    print("Resultado:")
    print(f"  Número:      {number}")
    print(f"  Comprimento: {details['length']}")
    print(f"  IIN Prefix:  {details['iin_prefix']}")
    print(f"  Luhn válido: {luhn_ok}")
    print(f"  Bandeira:    {brand if brand else 'Não identificada ou inválida'}")


if __name__ == "__main__":
    raise SystemExit(main())
