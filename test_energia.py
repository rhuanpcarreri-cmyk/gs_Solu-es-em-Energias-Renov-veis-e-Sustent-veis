"""[ENERGIA] Testes automáticos dos cálculos. Rodar: py test_energia.py"""
from energia import DadosEnergia, consumo_kwh_mes, comparar, cenario_padrao


def principal():
    dados = DadosEnergia("data/energia_dados.json")
    assert dados.carregar(), "dados de energia não carregaram"

    # fórmula básica: 5500 W, 10 min, 1 banho/dia, 30 dias = 27,5 kWh
    assert abs(consumo_kwh_mes(5500, 10, 1, 30) - 27.5) < 1e-9

    # (moradores, economia B/mês, economia C/mês, payback C em meses, CO2 B kg/ano)
    esperado = {1: (7.67, 17.90, 187.5, 3.8), 2: (15.35, 35.80, 93.8, 7.6),
                3: (23.02, 53.71, 62.5, 11.4), 4: (30.69, 71.61, 46.9, 15.2)}
    for moradores, (eb, ec, pb, co2) in esperado.items():
        c = cenario_padrao(dados)
        c["moradores"] = moradores
        a, b, s = comparar(c, dados)
        assert abs(b["economia_mes"] - eb) < 0.01, (moradores, "B", b["economia_mes"])
        assert abs(s["economia_mes"] - ec) < 0.01, (moradores, "C", s["economia_mes"])
        assert abs(s["payback_meses"] - pb) < 0.1, (moradores, "payback", s["payback_meses"])
        assert abs(b["co2_evitado_kg_ano"] - co2) < 0.05, (moradores, "co2", b["co2_evitado_kg_ano"])
        assert a["economia_mes"] == 0

    # imóvel alugado: aquecedor solar com viabilidade baixa
    c = cenario_padrao(dados)
    c["imovel_proprio"] = False
    assert comparar(c, dados)[2]["viabilidade"].startswith("BAIXA")

    # imóvel próprio com 4 pessoas: retorno em até 5 anos
    c = cenario_padrao(dados)
    c["moradores"] = 4
    assert comparar(c, dados)[2]["viabilidade"].startswith("MÉDIA-ALTA")

    # bandeira vermelha 2 aumenta o custo da referência
    c1 = cenario_padrao(dados)
    c2 = cenario_padrao(dados)
    c2["bandeira"] = "vermelha2"
    assert comparar(c2, dados)[0]["custo_mes"] > comparar(c1, dados)[0]["custo_mes"]

    print("Todos os testes de energia passaram.")


if __name__ == "__main__":
    principal()
