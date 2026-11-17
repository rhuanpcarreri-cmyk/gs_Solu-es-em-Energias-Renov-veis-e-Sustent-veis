import os

from base_conhecimento import BaseConhecimento
from assistente import Assistente
from energia import DadosEnergia


def main():
    # Garante que os caminhos "data/..." funcionem de qualquer pasta.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar o assistente sem a base de conhecimento.")
        return

    dados_energia = DadosEnergia("data/energia_dados.json")
    if not dados_energia.carregar():
        dados_energia = None  # o assistente funciona sem a simulação de energia

    assistente = Assistente("Citizen Assist AI", base, dados_energia=dados_energia)
    assistente.perguntar()


if __name__ == "__main__":
    main()
