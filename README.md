--- Credit Card Detector
Aplicação simples e funcional para identificar a bandeira de um cartão de crédito  (Visa, MasterCard, Amex, Discover, Diners, JCB, Elo, Hipercard, Aura) com base no número do cartão.  
O projeto também valida o número utilizando o algoritmo de Luhn, garantindo que o cartão segue a regra matemática de verificação.

--- Funcionalidades
- Identificação automática da bandeira do cartão pelo prefixo (IIN/BIN) e comprimento.
- Validação do número pelo algoritmo de Luhn.
- Interface de linha de comando (CLI) interativa.
- Uso como biblioteca em outros projetos.
- Testes automatizados com pytest.

--- CLI (linha de comando)
-- Executar diretamente passando o número do cartão:
- bash
python -m src.cli 4111111111111111
Saída esperada:

Código
Resultado:
  Número:      4111111111111111
  Comprimento: 16
  IIN Prefix:  411111
  Luhn válido: True
  Bandeira:    Visa
Modo interativo:

--- Testes
-- Rodar testes automatizados com pytest:
- bash
pytest -q

--- Limitações
Faixas IIN/BIN podem variar por emissor/região (especialmente Elo/Hipercard/Aura).
Validação Luhn não garante que o cartão exista, apenas que segue a regra matemática.
