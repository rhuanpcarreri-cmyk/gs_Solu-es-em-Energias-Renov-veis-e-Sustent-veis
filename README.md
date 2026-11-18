# Citizen Assist AI – Módulo de Energia

**GS 2026.2 – Soluções em Energias Renováveis e Sustentáveis (FIAP)**

Contribuição de energia ao assistente de terminal Citizen Assist AI (Python, apenas biblioteca padrão). O assistente-base foi criado na GS de Pensamento Computacional e Automação com Python; **toda a contribuição desta disciplina está marcada com [ENERGIA]** e listada abaixo.

## Integrantes
| Nome | RM |
|---|---|
| Rhuan Pacheco Carreri | 570129 |
| Fabio Pena Vieira | 570441 |

## Público e problema
**Público:** jovens no primeiro emprego (a partir de 16 anos), sozinhos ou em república, que passam a pagar a própria conta de luz.
**Problema:** o banho quente com chuveiro elétrico (5.500 W) é um dos maiores consumos da casa. Quanto isso custa e o que dá para fazer a respeito?

## Funcionalidades de energia
- **Menu 5 – Simulação:** o usuário informa pessoas, minutos de banho, potência do chuveiro, tarifa da fatura, bandeira tarifária e se o imóvel é próprio. O assistente compara 3 alternativas no mesmo período (1 mês) e mostra consumo, custo, economia, retorno do investimento, CO2 evitado, viabilidade, recomendação e limitações.
- **Menu 1 – Perguntas:** orientações 17 a 22 sobre consumo do chuveiro, encurtar o banho, aquecedor solar, bandeiras tarifárias, CO2 e energia para quem mora de aluguel, cada uma com fonte e data de verificação.
- **Alternativas comparadas:** A) chuveiro elétrico como está (referência); B) encurtar o banho em 3 minutos (eficiência); C) aquecedor solar de água (**fonte renovável**).

## Como executar e testar
Requer Python 3.8+ (sem instalar bibliotecas).
```bash
py main.py            # no Windows (ou: python main.py)
py test_energia.py    # testes automáticos dos cálculos
```
Para ver a energia: no menu, digite `5` e use Enter nos valores sugeridos, ou digite `1` e pergunte "quanto gasta o chuveiro eletrico".

## Resultado em resumo (bandeira verde, banho de 10 min, tarifa R$ 0,93/kWh)
| Pessoas | Custo do banho/mês | B: economia/mês | C: economia/mês | C: retorno |
|---|---|---|---|---|
| 1 | R$ 25,58 | R$ 7,67 | R$ 17,90 | 15,6 anos |
| 4 | R$ 102,30 | R$ 30,69 | R$ 71,61 | 3,9 anos |

Recomendação: começar por encurtar o banho; o aquecedor solar compensa em casa própria com várias pessoas e não para quem mora sozinho ou de aluguel. Todos os valores são **estimativas**, não garantias.

## Onde está cada requisito
| Requisito | Onde |
|---|---|
| Contexto, público e necessidade | `docs/energia/01_contexto_e_publico.md` |
| Dados, origem, unidades e premissas | `docs/energia/02_dados_e_premissas.md` e `data/energia_dados.json` |
| Cálculos e comparação das alternativas | `docs/energia/03_calculos_e_comparacao.md` e `energia.py` |
| Justificativas, custos, viabilidade, impacto ambiental e limitações | `docs/energia/04_recomendacoes_e_limitacoes.md` |
| Referências | `docs/energia/05_referencias.md` |
| Testes com usuários e ajustes | `docs/energia/06_testes_usuarios.md` |
| Integração ao assistente | menu 5 e orientações 17 a 22 (`assistente.py`, `data/base_conhecimento.json`) |

## Estrutura
```
├── main.py                  # ponto de entrada
├── energia.py               # [ENERGIA] fórmulas e comparação de alternativas
├── test_energia.py          # [ENERGIA] testes dos cálculos
├── assistente.py            # menu do assistente (inclui simular_energia, menu 5)
├── base_conhecimento.py     # busca por palavras-chave (projeto-base)
├── orientacao.py            # classe Orientacao (projeto-base)
├── data/
│   ├── energia_dados.json   # [ENERGIA] parâmetros com origem, fonte e premissa
│   ├── base_conhecimento.json  # 22 orientações: 16 de cidadania (base) + 6 de energia
│   └── historico.json       # atendimentos registrados
└── docs/energia/            # [ENERGIA] documentação da GS
```

## Testes com usuários
Em 17/11/2026, 3 pessoas de fora do grupo usaram o menu 1 e o menu 5, sem registro de nomes. Todas entenderam os resultados e nenhuma pediu mudanças. Detalhes e ajuste feito pela equipe em `docs/energia/06_testes_usuarios.md`.

## Limitações
As economias, o custo e a fração solar (70%) são estimativas que dependem de sol, telhado, hábito e tarifa. A tarifa de referência é anterior ao reajuste de julho/2026 da Enel SP, então o usuário deve usar a tarifa da própria fatura. Veja todas em `docs/energia/04_recomendacoes_e_limitacoes.md`.

## Projeto-base
O assistente-base (Citizen Assist AI) responde dúvidas de jovens no primeiro emprego sobre documentos e direitos de trabalho (ODS 8 e 16), com 16 orientações de fonte oficial. A parte de energia contribui também para o **ODS 7** (energia limpa e acessível). A regra de busca por palavras-chave é a mesma para todas as orientações.
