# [ENERGIA] 2. Dados utilizados, origem e premissas

Todos os dados ficam em `data/energia_dados.json`, cada um com valor, unidade, **tipo** (dado oficial, dado de mercado ou estimado), origem, fonte e premissa. Dados estimados estão identificados como tal.

| Parâmetro | Valor | Unidade | Tipo | Origem |
|---|---|---|---|---|
| Tarifa | 0,93 | R$/kWh (com tributos) | dado real arredondado | Fatura residencial B1 da Enel SP (fev/2026): TUSD 0,55437 + TE 0,37527 |
| Adicional de bandeira | 0 / 0,01885 / 0,04463 / 0,07877 | R$/kWh (sem tributos) | dado oficial | ANEEL: R$ 1,885, 4,463 e 7,877 a cada 100 kWh (verde, amarela, vermelha 1 e 2) |
| Potência do chuveiro | 5.500 | W | dado de mercado | Potência comum de chuveiros de 127 V |
| Dias por mês | 30 | dias | premissa | 1 banho por pessoa por dia |
| Duração do banho | 10 | min | premissa | Valor inicial, o usuário pode trocar |
| Redução do banho | 3 | min | estimado | Meta realista; a Cemig usa 4 min como exemplo |
| Fator de emissão da rede | 0,0385 | kg CO2/kWh | dado oficial | MCTI: 38,5 kg CO2/MWh em 2023 |
| Custo do aquecedor solar | 3.356,85 | R$ | referência de preço | SINAPI 103517 (jan/2026): 1 coletor, reservatório de 200 L, instalado |
| Área do coletor | 2,0 | m² | referência de catálogo | Kit de 200 L (SINAPI 34472) |
| Rendimento do coletor | 81,8 | kWh/mês por m² | dado de fabricante | Datasheet de coletor classe A (Komeco); o Inmetro exige no mínimo 52,3 |
| Fração solar | 70% | da energia do banho | **estimado** | Material de aquecimento solar (UNIPAMPA), conferido pela equipe |
| Limite de banhos do kit | 5 | banhos/dia | referência de catálogo | Kit de 200 L: 4 a 5 banhos/dia |
| Limite de retorno | 60 | meses | premissa da equipe | Critério nosso: compensa se se paga em até 5 anos |
| Horizonte | 10 | anos | premissa da equipe | Sem reajuste de tarifa e sem manutenção |

**Período de referência comum:** 1 mês (30 dias), mesma tarifa, mesma bandeira e mesma necessidade (banho quente) para as três alternativas. O custo do investimento é comparado em anos (retorno) e em 10 anos (economia líquida).

Os links completos estão em `data/energia_dados.json` e em `05_referencias.md`.
