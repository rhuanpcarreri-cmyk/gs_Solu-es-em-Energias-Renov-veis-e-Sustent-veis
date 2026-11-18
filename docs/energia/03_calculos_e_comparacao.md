# [ENERGIA] 3. Cálculos e comparação das alternativas

## Fórmulas
- **Energia:** kWh = (potência em W ÷ 1000) × horas.
- **Custo mensal:** kWh × tarifa efetiva (tarifa + adicional da bandeira).
- **Retorno (payback):** investimento ÷ economia mensal.
- **Economia líquida em 10 anos:** economia mensal × 12 × 10 − investimento.
- **CO2 evitado:** kWh economizados × 12 × 0,0385 kg/kWh.

## Alternativas (mesma necessidade: banho quente; período: 1 mês)
- **A) Chuveiro elétrico como está** (referência).
- **B) Encurtar o banho em 3 minutos** (eficiência energética, sem custo).
- **C) Aquecedor solar de água** (fonte renovável): o sol cobre 70% da energia do banho; o resto vem da rede.

## Exemplo conferido à mão (1 pessoa, banho de 10 min, 5.500 W, tarifa R$ 0,93, bandeira verde)
- A: 5,5 kW × (10/60 h) × 30 = **27,5 kWh/mês** → 27,5 × 0,93 = **R$ 25,58**.
- B: 5,5 × (7/60) × 30 = 19,25 kWh → economia de 8,25 kWh = **R$ 7,67/mês** (R$ 92,07/ano). CO2 evitado: 8,25 × 12 × 0,0385 = **3,8 kg/ano**.
- C: 27,5 × 0,70 = 19,25 kWh vêm do sol (abaixo do limite do coletor, 81,8 × 2,0 = 163,6 kWh) → economia de 19,25 kWh = **R$ 17,90/mês** (R$ 214,83/ano). Retorno: 3.356,85 ÷ 17,90 = 187,5 meses = **15,6 anos**. CO2 evitado: 19,25 × 12 × 0,0385 = **8,9 kg/ano**.

## Resultados por número de pessoas (bandeira verde; o programa calcula exatamente esses valores)
| Pessoas | A: kWh/mês | A: custo/mês | B: economia/mês | B: CO2 (kg/ano) | C: economia/mês | C: retorno | C: economia líquida em 10 anos | C: CO2 (kg/ano) |
|---|---|---|---|---|---|---|---|---|
| 1 | 27,5 | R$ 25,58 | R$ 7,67 | 3,8 | R$ 17,90 | 15,6 anos | −R$ 1.209 | 8,9 |
| 2 | 55,0 | R$ 51,15 | R$ 15,35 | 7,6 | R$ 35,80 | 7,8 anos | +R$ 940 | 17,8 |
| 3 | 82,5 | R$ 76,73 | R$ 23,02 | 11,4 | R$ 53,71 | 5,2 anos | +R$ 3.088 | 26,7 |
| 4 | 110,0 | R$ 102,30 | R$ 30,69 | 15,2 | R$ 71,61 | 3,9 anos | +R$ 5.236 | 35,6 |

B em 10 anos (sem custo): +R$ 921 (1 pessoa) a +R$ 3.683 (4 pessoas).

## Custos, viabilidade e impacto ambiental
| | Custo inicial | Viabilidade | Impacto ambiental |
|---|---|---|---|
| A | nenhum | referência | referência |
| B | nenhum | alta, depende do hábito | pequeno: evita 3,8 a 15,2 kg CO2/ano |
| C | R$ 3.356,85 | baixa para 1 a 3 pessoas ou imóvel alugado; média-alta para 4 pessoas em casa própria (retorno ≤ 5 anos) | maior que B (8,9 a 35,6 kg CO2/ano), mas ainda pequeno, porque a rede elétrica brasileira já emite pouco |

## Verificação
Os cálculos são executados e conferidos pelos testes automáticos (`py test_energia.py`), que comparam os resultados do programa com os valores desta tabela.
