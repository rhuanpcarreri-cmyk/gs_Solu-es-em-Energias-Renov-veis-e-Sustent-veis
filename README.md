# Citizen Assist AI

Assistente de terminal em Python (apenas biblioteca padrão) que responde dúvidas de cidadãos a partir de uma base de conhecimento em JSON, com fonte oficial e data de verificação em toda resposta.

**GS 2026.2 – Pensamento Computacional e Automação com Python (FIAP) – desafio CitizenTech**

## Integrantes
| Nome | RM |
|---|---|
| Rhuan Pacheco Carreri | 570129 |
| Fabio Pena Vieira | 570441 |

## Público atendido
Jovens no primeiro emprego (a partir de 16 anos) que precisam organizar documentos, entender direitos básicos de trabalho e não cair em golpes de vaga falsa.

## Problema
Quem começa a trabalhar costuma ter dúvidas simples (CPF, Carteira de Trabalho Digital, título de eleitor, seguro-desemprego, férias, 13º) e encontra informação espalhada em vários sites, em linguagem difícil ou em fontes não oficiais. O assistente reúne respostas curtas, em linguagem simples, sempre com a fonte oficial para o usuário conferir.

## ODS relacionados
- **ODS 8** – Trabalho decente e crescimento econômico (direitos trabalhistas, jovem aprendiz, vagas, golpes de emprego).
- **ODS 16** – Paz, justiça e instituições eficazes (acesso à informação pública e a serviços do governo).

## Como executar
Requer Python 3.8+ (sem instalar nada).
```bash
python main.py
```
Menu: `1` fazer uma pergunta · `2` navegar por categoria · `3` ver indicadores · `4` exportar CSV · `5` simular economia de energia (GS Energias Renováveis) · `0` sair.
Em todas as telas, `0` volta.

## Estrutura
```
citizen-assist-ai/
├── main.py                  # ponto de entrada
├── orientacao.py            # classe Orientacao (exibir)
├── base_conhecimento.py     # BaseConhecimento (carregar, categorias, por_categoria, pontuar, buscar)
├── assistente.py            # Assistente (perguntar, navegar, registrar, indicadores, exportar_csv, simular_energia)
├── energia.py               # [ENERGIA] fórmulas e comparação de alternativas
├── docs/energia/            # [ENERGIA] documentação da GS Energias Renováveis
└── data/
    ├── base_conhecimento.json   # 22 orientações, 5 categorias (6 novas em Energia)
    ├── energia_dados.json       # [ENERGIA] parâmetros com origem, fonte e premissa
    ├── historico.json           # atendimentos registrados
    └── atendimentos.csv         # exportação do histórico
```
Composição: `Assistente` → `BaseConhecimento` → lista de `Orientacao`.

## Regra de pontuação
O texto da pergunta e as palavras-chave são normalizados (minúsculas, sem acento, sem pontuação).
- **+3 pontos** por palavra-chave da orientação encontrada na pergunta.
- **+1 ponto** por palavra da pergunta com 4+ letras que aparece no título (palavras muito comuns como "como", "para", "quero" não pontuam).
- **6 ou mais** → confiança **ALTA**. **3 a 5** → **MÉDIA** (o assistente avisa que não tem certeza). **Menos de 3** → "Não encontrei", com sugestão de outras palavras e das categorias.
- Mostra a melhor orientação e até 2 alternativas (só se tiverem pelo menos 3 pontos).

## Segurança e privacidade
- Nunca pede nome, CPF, telefone ou e-mail.
- Pergunta com 8 ou mais dígitos ou com "@" é recusada e **não** é gravada.
- Entradas inválidas (letras, vazio, opção inexistente, s/n errado) não encerram o programa.
- Base ausente ou corrompida: mensagem de erro, sem travar. Histórico corrompido: é renomeado para `.corrompido` e começa um novo.
- Toda resposta traz fonte, data de verificação e o aviso "este assistente não é canal oficial".

## Indicadores
Calculados a partir de `data/historico.json` (menu 3): % de respostas encontradas, tempo médio, facilidade de uso média (nota 1–5 pedida ao sair), taxa de acerto (ajudou), tentativas por atendimento e lista de dúvidas sem solução. O menu 4 exporta tudo para `data/atendimentos.csv`.

## Integrações
Nenhuma integração externa em tempo real. O assistente funciona offline com a base JSON. As fontes oficiais ficam no campo `fonte` de cada orientação e foram consultadas em 16/11/2026.

## Fontes oficiais (base verificada em 16/11/2026)
- CPF: https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf
- Carteira de Trabalho Digital: https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
- Título de eleitor (TSE): https://www.tse.jus.br/comunicacao/noticias/2024/Abril/precisa-ir-ao-cartorio-eleitoral-confira-os-documentos-que-voce-deve-levar
- Alistamento militar: https://www.gov.br/defesa/pt-br/assuntos/servico-militar
- Carteira de Identidade Nacional: https://www.gov.br/governodigital/pt-br/identidade/cin
- Seguro-desemprego: https://www.gov.br/pt-br/temas/perguntas-frequentes-seguro-desemprego
- Jovem Aprendiz: https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2026/julho/aprendizagem-profissional-regras-direitos-e-funcionamento-do-contrato-de-aprendizagem
- Sine: https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine
- FGTS: https://www.fgts.gov.br/Paginas/trabalhador/app-fgts.aspx
- Jornada, hora extra e férias: https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/trabalho-sustentavel/trabalhadores-e-trabalhadoras
- 13º salário: https://www3.mte.gov.br/ouvidoria/duvidas_trabalhistas.asp
- Central 158 / denúncias: https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2023/marco/central-alo-trabalho-158
- Golpe de vaga falsa (alerta do MTE): https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2025/setembro/mte-alerta-e-falsa-a-informacao-sobre-processos-seletivos-para-vagas-nos-correios
- Consumidor.gov.br: https://www.gov.br/pt-br/servicos/reclamar-contra-servico-ou-produto-de-empresas-privadas
- Níveis da conta gov.br: https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/niveis-da-conta-govbr
- Meu INSS / CNIS: https://www.gov.br/inss/pt-br/noticias/saiba-como-consultar-extratos-de-contribuicoes-pelo-site-ou-aplicativo-meu-inss

## Resultado do teste com usuários
- **Módulo de energia (GS Energias Renováveis):** teste em 17/11/2026 com 3 pessoas de fora do grupo. Todas entenderam os resultados e ninguém pediu mudanças. Detalhes em `docs/energia/teste_usuarios_energia.md`.
- **Base de cidadania (GS Pensamento Computacional):** indicadores gerados pelo menu 3 em `data/historico.json` e `data/atendimentos.csv` quando o assistente é usado.

## Limitações
- A busca é por palavras-chave: perguntas com sinônimos que não estão na base podem não ser encontradas (por isso o "Não encontrei" com sugestões).
- A base tem 22 orientações (16 de cidadania e 6 de energia); regras e prazos podem mudar, por isso cada uma mostra a data de verificação.
- Algumas regras variam por estado (ex.: agendamento da CIN e do título de eleitor). O assistente indica onde confirmar.
- Não é canal oficial e não substitui o atendimento do órgão responsável.

## Contribuição para a GS Soluções em Energias Renováveis e Sustentáveis
Esta parte foi adicionada ao mesmo projeto e está identificada em todo o repositório com a marca **[ENERGIA]**.

- **Necessidade:** jovens no primeiro emprego (sozinhos ou em república) querem reduzir a conta de luz, e o chuveiro elétrico é um dos maiores consumos da casa.
- **Alternativas comparadas (mesmo período de 1 mês, mesma tarifa):** A) chuveiro elétrico como está (referência); B) encurtar o banho em 3 minutos (eficiência); C) aquecedor solar de água (renovável).
- **No assistente:** menu `5` pede pessoas, minutos, potência, tarifa, bandeira e se o imóvel é próprio, e mostra consumo, custo, economia, retorno do investimento, CO2 evitado e viabilidade. As perguntas de energia no menu `1` (ids 17 a 22) usam os mesmos números.
- **Arquivos:** `energia.py`, `data/energia_dados.json`, orientações 17 a 22 em `data/base_conhecimento.json` e a pasta `docs/energia/` (análise de consumo, comparação, premissas, referências, limitações e teste com usuários).
- Todas as economias são **estimativas**, com premissas e fontes registradas em `data/energia_dados.json`.

## Vídeo técnico
Link (YouTube, não listado): __
