"""Módulo de energia do Citizen Assist AI.

Contribuição da disciplina Soluções em Energias Renováveis e Sustentáveis.
Necessidade analisada: custo do banho quente de jovens no primeiro emprego.
Compara 3 alternativas para a mesma necessidade e o mesmo período:
  A) manter o chuveiro elétrico como está (referência)
  B) encurtar o banho (eficiência, custo zero)
  C) aquecedor solar de água (fonte renovável)
Todos os parâmetros vêm de data/energia_dados.json, com origem e premissa.
"""

import json

BANDEIRAS = ["verde", "amarela", "vermelha1", "vermelha2"]


class DadosEnergia:
    def __init__(self, caminho):
        self.caminho = caminho
        self.parametros = {}

    def carregar(self):
        """Lê o JSON de parâmetros. Devolve True/False sem derrubar o programa."""
        try:
            with open(self.caminho, encoding="utf-8") as arq:
                dados = json.load(arq)
            self.parametros = dados["parametros"]
            # confere que todos os parâmetros usados existem
            for nome in ("tarifa_kwh", "bandeira_adicional_por_kwh", "potencia_chuveiro_w",
                         "dias_mes", "reducao_minutos_banho", "fator_emissao_kg_kwh",
                         "custo_aquecedor_solar_rs", "area_coletor_m2", "pmee_kwh_mes_m2",
                         "fracao_solar", "limite_banhos_dia_kit", "limite_payback_meses",
                         "horizonte_anos"):
                self.parametros[nome]["valor"]
        except FileNotFoundError:
            print(f"[ERRO] Dados de energia não encontrados: {self.caminho}")
            return False
        except (json.JSONDecodeError, KeyError, TypeError):
            print(f"[ERRO] Dados de energia corrompidos ou incompletos: {self.caminho}")
            return False
        return True

    def valor(self, nome):
        return self.parametros[nome]["valor"]


# ----------------------------------------------------------------- fórmulas
def consumo_kwh_mes(potencia_w, minutos_por_banho, banhos_por_dia, dias):
    """Energia = potência (kW) x tempo (h). Resultado em kWh por mês."""
    return (potencia_w / 1000) * (minutos_por_banho / 60) * banhos_por_dia * dias


def tarifa_efetiva(tarifa_base, bandeira, dados):
    """Tarifa por kWh somando o adicional da bandeira tarifária."""
    return tarifa_base + dados.valor("bandeira_adicional_por_kwh")[bandeira]


def _resultado(nome, tipo, investimento, kwh_rede_mes, kwh_base_mes, tarifa, fator, horizonte):
    """Monta o resultado de uma alternativa em relação à referência (alternativa A)."""
    custo_mes = kwh_rede_mes * tarifa
    economia_kwh = kwh_base_mes - kwh_rede_mes
    economia_mes = economia_kwh * tarifa
    payback = None
    if investimento > 0 and economia_mes > 0:
        payback = investimento / economia_mes
    return {
        "nome": nome,
        "tipo": tipo,
        "investimento": investimento,
        "kwh_rede_mes": kwh_rede_mes,
        "custo_mes": custo_mes,
        "economia_kwh_mes": economia_kwh,
        "economia_mes": economia_mes,
        "economia_ano": economia_mes * 12,
        "payback_meses": payback,
        "economia_liquida_horizonte": economia_mes * 12 * horizonte - investimento,
        "co2_evitado_kg_ano": economia_kwh * 12 * fator,
        "viabilidade": "",
        "observacoes": [],
    }


def comparar(cenario, dados):
    """Compara as alternativas A, B e C para o mesmo cenário.

    cenario: dict com moradores, minutos_banho, potencia_w, tarifa_base, bandeira, imovel_proprio.
    Devolve lista de 3 dicionários (A, B, C) e as premissas usadas.
    """
    banhos_dia = cenario["moradores"]  # 1 banho por morador por dia
    dias = dados.valor("dias_mes")
    tarifa = tarifa_efetiva(cenario["tarifa_base"], cenario["bandeira"], dados)
    fator = dados.valor("fator_emissao_kg_kwh")
    horizonte = dados.valor("horizonte_anos")

    kwh_a = consumo_kwh_mes(cenario["potencia_w"], cenario["minutos_banho"], banhos_dia, dias)

    # A) referência: chuveiro elétrico sem mudanças
    a = _resultado("A) Chuveiro elétrico como está", "referência", 0.0, kwh_a, kwh_a, tarifa, fator, horizonte)
    a["viabilidade"] = "Referência"
    a["observacoes"].append("Alternativa de comparação: não gera economia.")

    # B) encurtar o banho (eficiência, sem custo)
    minutos_b = max(cenario["minutos_banho"] - dados.valor("reducao_minutos_banho"), 0)
    kwh_b = consumo_kwh_mes(cenario["potencia_w"], minutos_b, banhos_dia, dias)
    b = _resultado(f"B) Encurtar o banho em {dados.valor('reducao_minutos_banho')} min", "eficiência",
                   0.0, kwh_b, kwh_a, tarifa, fator, horizonte)
    b["viabilidade"] = "ALTA (depende só do hábito)"
    b["observacoes"].append("Sem custo de instalação. Exige disciplina e depende do conforto de cada pessoa.")

    # C) aquecedor solar de água (renovável)
    producao_mes = dados.valor("pmee_kwh_mes_m2") * dados.valor("area_coletor_m2")
    economia_kwh_c = min(kwh_a * dados.valor("fracao_solar"), producao_mes)
    kwh_c = kwh_a - economia_kwh_c
    c = _resultado("C) Aquecedor solar de água (renovável)", "renovável",
                   dados.valor("custo_aquecedor_solar_rs"), kwh_c, kwh_a, tarifa, fator, horizonte)
    limite_pb = dados.valor("limite_payback_meses")
    if not cenario["imovel_proprio"]:
        c["viabilidade"] = "BAIXA (imóvel alugado)"
        c["observacoes"].append("Precisa de telhado e autorização do proprietário. O investimento fica no imóvel.")
    elif c["payback_meses"] is None:
        c["viabilidade"] = "BAIXA (sem economia)"
    elif c["payback_meses"] <= limite_pb:
        c["viabilidade"] = "MÉDIA-ALTA (retorno em até 5 anos)"
    else:
        c["viabilidade"] = "BAIXA (retorno acima de 5 anos)"
    if banhos_dia > dados.valor("limite_banhos_dia_kit"):
        c["observacoes"].append(
            f"O kit de 200 L atende até {dados.valor('limite_banhos_dia_kit')} banhos por dia. "
            "Para mais pessoas seria preciso um sistema maior, com custo maior que o calculado.")
    c["observacoes"].append("Economia estimada: depende de sol, inclinação, sombra e estação. Não é garantida.")

    return [a, b, c]


def recomendar(resultados, cenario, dados):
    """Texto da recomendação, coerente com os números calculados."""
    b, c = resultados[1], resultados[2]
    limite_pb = dados.valor("limite_payback_meses")
    linhas = []
    if b["economia_mes"] > 0:
        linhas.append(f"1) Comece por encurtar o banho: economiza cerca de R$ {b['economia_mes']:.2f} por mês, sem gastar nada.")
    if not cenario["imovel_proprio"]:
        linhas.append("2) Aquecedor solar: só vale conversar com o proprietário se o imóvel for ficar com você por muitos anos.")
    elif c["payback_meses"] is not None and c["payback_meses"] <= limite_pb:
        linhas.append(f"2) Vale pedir orçamento de aquecedor solar: o retorno estimado é de {c['payback_meses'] / 12:.1f} anos.")
    elif c["payback_meses"] is not None:
        linhas.append(f"2) Aquecedor solar não compensa financeiramente para esse uso: o retorno estimado seria de {c['payback_meses'] / 12:.1f} anos.")
    return linhas


def cenario_padrao(dados):
    return {"moradores": 1, "minutos_banho": 10, "potencia_w": dados.valor("potencia_chuveiro_w"),
            "tarifa_base": dados.valor("tarifa_kwh"), "bandeira": "verde", "imovel_proprio": True}
