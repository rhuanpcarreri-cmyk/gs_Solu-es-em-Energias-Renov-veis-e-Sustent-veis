# [ENERGIA] Análise de energia: banho quente do jovem no primeiro emprego

Contribuição da GS **Soluções em Energias Renováveis e Sustentáveis** ao Citizen Assist AI.
Integrantes: Rhuan Pacheco Carreri (RM 570129) e Fabio Pena Vieira (RM 570441).

## 1. Necessidade e público
Jovens no primeiro emprego, morando sozinhos ou em república, querem reduzir a conta de luz. O chuveiro elétrico (5.500 W) é um dos maiores consumos de uma casa.

## 2. Análise de consumo
Fórmula: **kWh = (potência em W ÷ 1000) × horas**. Custo = kWh × tarifa.

Cenário padrão (1 pessoa, banho de 10 min, 5.500 W, 30 dias, tarifa R$ 0,93/kWh, bandeira verde):
- Consumo: 5,5 kW × (10/60 h) × 30 = **27,5 kWh/mês**
- Custo: 27,5 × 0,93 = **R$ 25,58/mês**

O consumo cresce de forma proporcional ao número de pessoas (4 pessoas: 110 kWh, R$ 102,30/mês).

## 3. Alternativas comparadas (mesmo período: 1 mês; mesma tarifa)
| Alternativa | Tipo | Investimento | Economia/mês (1 pessoa) | Economia/mês (4 pessoas) | Retorno (1 / 4 pessoas) |
|---|---|---|---|---|---|
| A) Chuveiro como está | referência | 0 | 0 | 0 | não se aplica |
| B) Encurtar o banho em 3 min | eficiência | 0 | R$ 7,67 | R$ 30,69 | imediato |
| C) Aquecedor solar de água | renovável | R$ 3.356,85 | R$ 17,90 | R$ 71,61 | 15,6 anos / 3,9 anos |

Economia líquida em 10 anos (sem reajuste e sem manutenção): C = −R$ 1.209 (1 pessoa), +R$ 5.236 (4 pessoas). B = +R$ 921 e +R$ 3.683.

## 4. Cálculo das alternativas
- **B:** 5,5 kW × (7/60 h) × 30 = 19,25 kWh. Economia = 27,5 − 19,25 = 8,25 kWh × 0,93 = R$ 7,67.
- **C:** o sol cobre 70% da energia do banho (estimado). 27,5 × 0,70 = 19,25 kWh. Limite físico do coletor: 81,8 kWh/mês/m² × 2,0 m² = 163,6 kWh (não limita neste cenário). Rede passa a 8,25 kWh = R$ 7,67/mês. Economia = R$ 17,90/mês.
- **Retorno (payback):** investimento ÷ economia mensal = 3.356,85 ÷ 17,90 = 187,5 meses (15,6 anos) para 1 pessoa; 3.356,85 ÷ 71,61 = 46,9 meses (3,9 anos) para 4 pessoas.
- **CO2 evitado:** kWh economizados × 12 × 0,0385 kg/kWh. B (1 pessoa): 8,25 × 12 × 0,0385 = 3,8 kg/ano.

## 5. Justificativa da recomendação
1. **B vem primeiro:** custo zero, efeito imediato. Mesmo valendo pouco para 1 pessoa, vale para todos.
2. **C só compensa em certas condições:** casa própria e várias pessoas (retorno abaixo de 5 anos, critério da equipe). Para quem mora sozinho ou de aluguel, não compensa. O assistente diz isso nas respostas.
3. **O ganho ambiental é pequeno** porque a rede elétrica brasileira já é limpa (38,5 kg CO2/MWh em 2023). O principal benefício é financeiro.

## 6. Integração com o assistente
- Menu `5`: simulação com os dados do próprio usuário (pessoas, minutos, potência, tarifa, bandeira, imóvel próprio ou alugado).
- Menu `1`: orientações 17 a 22 (consumo do chuveiro, encurtar o banho, aquecedor solar, bandeiras, CO2, aluguel), com fonte e data de verificação (17/11/2026).

## 7. Parâmetros, tipo e fonte
| Parâmetro | Valor | Tipo | Fonte |
|---|---|---|---|
| Tarifa | R$ 0,93/kWh | dado real arredondado (fatura Enel SP, fev/2026, TUSD 0,55437 + TE 0,37527) | camara.leg.br (fatura) |
| Bandeiras | R$ 1,885 / 4,463 / 7,877 a cada 100 kWh | dado oficial | gov.br/aneel |
| Potência do chuveiro | 5.500 W | dado de mercado | Canaltech |
| Redução do banho | 3 min | estimado (Cemig usa 4 min como exemplo) | Diário de Pernambuco |
| Fator de emissão | 0,0385 kg CO2/kWh | dado oficial (MCTI, 2023) | eixos.com.br |
| Custo do aquecedor solar | R$ 3.356,85 | referência de preço (SINAPI 103517, jan/2026) | orcamentor.com |
| Rendimento do coletor | 81,8 kWh/mês/m² | dado de fabricante (classe A) | Komeco (datasheet) |
| Fração solar | 70% | **estimado** | material de aquecimento solar (UNIPAMPA) |
| Limite de retorno | 60 meses | premissa da equipe | n/a |

Os links completos estão em `data/energia_dados.json`.

## 8. Limitações
- Estimativas, não garantias. A economia real depende de sol, inclinação, sombra, estação e hábito.
- A tarifa e a bandeira mudam; o usuário deve usar os valores da própria fatura. A tarifa usada é anterior ao reajuste de 10,18% da Enel SP de julho/2026, então os valores reais tendem a ser um pouco maiores.
- O adicional da bandeira é somado sem tributos.
- Considera 1 banho por pessoa por dia, 30 dias por mês, sem reajuste de tarifa nem manutenção.
- O preço do aquecedor solar é de referência de obra pública (SINAPI); o orçamento real varia. Kit considerado: até 5 banhos por dia.
- Não inclui o CO2 de fabricação dos equipamentos.
- A fração solar de 70% é uma estimativa de literatura, não medida por nós.
- Alguns valores vêm de fontes secundárias (Canaltech, jornais, ABRAVA); por isso estão marcados como estimativa ou dado de mercado.
- Fonte de irradiação solar (CRESESB SunData) não foi usada nos cálculos; a fração solar a substitui como simplificação.

## 9. Uso de IA generativa
A IA ajudou a pesquisar fontes e organizar o código. Os dados, as fórmulas e as referências foram conferidos pela equipe, e os cálculos foram executados no programa e conferidos à mão.
