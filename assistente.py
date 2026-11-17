"""Assistente de terminal: perguntas, navegação por categoria, histórico e indicadores."""

import csv
import json
import os
import time
from datetime import datetime

import energia

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo", "facilidade"]
MIN_DIGITOS_BLOQUEIO = 8


class _Sair(Exception):
    """Entrada encerrada (Ctrl+C / Ctrl+D): sai do programa com educação."""


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv", dados_energia=None):
        self.nome = nome
        self.base = base
        self.dados_energia = dados_energia  # módulo de energia (pode ser None)
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = []
        self._sessao = []  # registros criados nesta execução
        self._carregar_historico()

    # ------------------------------------------------------------------ entrada
    def _entrada(self, texto):
        try:
            return input(texto).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raise _Sair()

    def _ler_opcao(self, texto, validas):
        while True:
            resp = self._entrada(texto)
            if resp in validas:
                return resp
            print(f"Opção inválida. Digite um destes valores: {', '.join(validas)}.")

    def _ler_sn(self, texto):
        while True:
            resp = self._entrada(texto).lower()
            if resp in ("s", "n"):
                return resp == "s"
            print("Responda apenas com 's' (sim) ou 'n' (não).")

    def _ler_texto(self, texto):
        while True:
            resp = self._entrada(texto)
            if resp:
                return resp
            print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")

    @staticmethod
    def _tem_dado_pessoal(texto):
        digitos = sum(c.isdigit() for c in texto)
        return digitos >= MIN_DIGITOS_BLOQUEIO or "@" in texto

    # ---------------------------------------------------------------- histórico
    def _carregar_historico(self):
        try:
            with open(self.caminho_historico, encoding="utf-8") as arq:
                dados = json.load(arq)
            if isinstance(dados, list):
                self.historico = [r for r in dados if isinstance(r, dict)]
            else:
                raise ValueError("formato inesperado")
        except FileNotFoundError:
            self.historico = []
        except (json.JSONDecodeError, ValueError, OSError):
            print("[AVISO] O histórico estava ilegível; começando um histórico novo.")
            try:
                os.replace(self.caminho_historico, self.caminho_historico + ".corrompido")
            except OSError:
                pass
            self.historico = []

    def _salvar_historico(self):
        try:
            pasta = os.path.dirname(self.caminho_historico)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho_historico, "w", encoding="utf-8") as arq:
                json.dump(self.historico, arq, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f"[AVISO] Não foi possível salvar o histórico: {erro}")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, inicio):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": round(time.time() - inicio, 1),
            "facilidade": None,
        }
        self.historico.append(registro)
        self._sessao.append(registro)
        self._salvar_historico()

    # ------------------------------------------------------------------- telas
    def perguntar(self):
        """Loop principal do assistente."""
        print(f"\nBem-vindo ao {self.nome}!")
        print("Respondo dúvidas sobre documentos, trabalho e direitos com base em fontes oficiais.")
        print("Não peço nome, CPF, telefone nem e-mail. Não digite dados pessoais.")
        try:
            while True:
                print("\n--- MENU ---")
                print("1 - Fazer uma pergunta")
                print("2 - Navegar por categoria")
                print("3 - Ver indicadores")
                print("4 - Exportar atendimentos para CSV")
                print("5 - Simular economia de energia no banho")
                print("0 - Sair")
                opcao = self._ler_opcao("Escolha: ", ["0", "1", "2", "3", "4", "5"])
                if opcao == "1":
                    self._atendimento_por_pergunta()
                elif opcao == "2":
                    self.navegar()
                elif opcao == "3":
                    self.indicadores()
                elif opcao == "4":
                    self.exportar_csv()
                elif opcao == "5":
                    self.simular_energia()
                else:
                    break
            self._avaliar_facilidade()
        except _Sair:
            print("Encerrando o assistente.")
        print("Obrigado por usar o assistente. Até a próxima!")

    def _mostrar_resultado(self, nivel, resultados):
        """Mostra a melhor orientação e até 2 alternativas. Devolve o id da orientação final vista."""
        melhor = resultados[0][1]
        print(f"\nConfiança da resposta: {nivel}")
        if nivel == "MÉDIA":
            print("(Não tenho certeza. Veja se é isso mesmo que você procura.)")
        melhor.exibir()
        id_visto = melhor.id
        alternativas = [o for _, o in resultados[1:]]
        while alternativas:
            print("Outras orientações que podem ajudar:")
            for i, o in enumerate(alternativas, 1):
                print(f"  {i} - {o.titulo} [{o.categoria}]")
            print("  0 - Continuar")
            escolha = self._ler_opcao("Ver alguma delas? ", [str(i) for i in range(len(alternativas) + 1)])
            if escolha == "0":
                break
            alternativa = alternativas[int(escolha) - 1]
            alternativa.exibir()
            id_visto = alternativa.id
        return id_visto

    def _sugestoes_sem_resposta(self):
        print("\nNão encontrei uma orientação confiável para essa pergunta.")
        print("Tente usar outras palavras (ex.: o nome do documento ou do serviço).")
        print("Ou escolha uma categoria no menu 2. Categorias disponíveis:")
        for cat in self.base.categorias():
            print(f"  - {cat}")

    def _atendimento_por_pergunta(self):
        inicio = time.time()
        tentativas = 0
        ultima = None
        encontrou = False
        ajudou = False
        id_final = None
        while True:
            texto = self._ler_texto("\nDigite sua dúvida (0 para voltar): ")
            if texto == "0":
                break
            if self._tem_dado_pessoal(texto):
                print("Por segurança não aceito números longos nem e-mails. "
                      "Reescreva a pergunta sem dados pessoais. (Essa mensagem não foi guardada.)")
                continue
            tentativas += 1
            ultima = texto
            nivel, resultados = self.base.buscar(texto)
            if not resultados:
                encontrou, ajudou, id_final = False, False, None
                self._sugestoes_sem_resposta()
            else:
                encontrou = True
                id_final = self._mostrar_resultado(nivel, resultados)
                ajudou = self._ler_sn("Essa resposta ajudou? (s/n): ")
                if ajudou:
                    break
            if not self._ler_sn("Quer tentar de novo com outras palavras? (s/n): "):
                break
        if tentativas > 0:
            self.registrar("pergunta", ultima, id_final, encontrou, ajudou, tentativas, inicio)

    def navegar(self):
        categorias = self.base.categorias()
        while True:
            print("\n--- CATEGORIAS ---")
            for i, cat in enumerate(categorias, 1):
                print(f"  {i} - {cat}")
            print("  0 - Voltar")
            validas = [str(i) for i in range(len(categorias) + 1)]
            escolha = self._ler_opcao("Escolha a categoria: ", validas)
            if escolha == "0":
                return
            categoria = categorias[int(escolha) - 1]
            self._navegar_categoria(categoria)

    def _navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n--- {categoria.upper()} ---")
            for i, o in enumerate(orientacoes, 1):
                print(f"  {i} - {o.titulo}")
            print("  0 - Voltar")
            validas = [str(i) for i in range(len(orientacoes) + 1)]
            escolha = self._ler_opcao("Escolha o assunto: ", validas)
            if escolha == "0":
                return
            inicio = time.time()
            orientacao = orientacoes[int(escolha) - 1]
            orientacao.exibir()
            ajudou = self._ler_sn("Essa resposta ajudou? (s/n): ")
            self.registrar("categoria", orientacao.titulo, orientacao.id, True, ajudou, 1, inicio)

    def _avaliar_facilidade(self):
        if not self._sessao:
            return
        print("\nDe 1 a 5, quão fácil foi usar o assistente? (1 = muito difícil, 5 = muito fácil)")
        nota = int(self._ler_opcao("Sua nota: ", ["1", "2", "3", "4", "5"]))
        for registro in self._sessao:
            registro["facilidade"] = nota
        self._salvar_historico()

    # -------------------------------------------------------------- indicadores
    def calcular_indicadores(self):
        total = len(self.historico)
        if total == 0:
            return None
        encontrados = [r for r in self.historico if r.get("encontrou")]
        ajudaram = [r for r in encontrados if r.get("ajudou")]
        notas = [r["facilidade"] for r in self.historico if isinstance(r.get("facilidade"), int)]
        sem_solucao = []
        for r in self.historico:
            if not r.get("encontrou") or not r.get("ajudou"):
                if r.get("pergunta") and r["pergunta"] not in sem_solucao:
                    sem_solucao.append(r["pergunta"])
        return {
            "total": total,
            "pct_encontrada": 100 * len(encontrados) / total,
            "tempo_medio": sum(r.get("tempo", 0) for r in self.historico) / total,
            "facilidade_media": (sum(notas) / len(notas)) if notas else None,
            "taxa_acerto": (100 * len(ajudaram) / len(encontrados)) if encontrados else 0.0,
            "tentativas_medias": sum(r.get("tentativas", 1) for r in self.historico) / total,
            "sem_solucao": sem_solucao,
        }

    def indicadores(self):
        ind = self.calcular_indicadores()
        print("\n--- INDICADORES ---")
        if ind is None:
            print("Ainda não há atendimentos registrados.")
            return
        print(f"Atendimentos registrados: {ind['total']}")
        print(f"Resposta encontrada: {ind['pct_encontrada']:.1f}%")
        print(f"Tempo médio por atendimento: {ind['tempo_medio']:.1f} s")
        if ind["facilidade_media"] is None:
            print("Facilidade de uso média: sem notas ainda")
        else:
            print(f"Facilidade de uso média: {ind['facilidade_media']:.1f} / 5")
        print(f"Taxa de acerto (ajudou, entre as respostas encontradas): {ind['taxa_acerto']:.1f}%")
        print(f"Tentativas por atendimento: {ind['tentativas_medias']:.2f}")
        print("Dúvidas sem solução:")
        if not ind["sem_solucao"]:
            print("  (nenhuma)")
        for pergunta in ind["sem_solucao"]:
            print(f"  - {pergunta}")

    def exportar_csv(self):
        if not self.historico:
            print("Não há atendimentos para exportar ainda.")
            return False
        try:
            pasta = os.path.dirname(self.caminho_csv)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arq:
                escritor = csv.DictWriter(arq, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                for registro in self.historico:
                    linha = {campo: registro.get(campo, "") for campo in CAMPOS_CSV}
                    for campo in ("encontrou", "ajudou"):
                        linha[campo] = "sim" if registro.get(campo) else "nao"
                    if linha["id_orientacao"] is None:
                        linha["id_orientacao"] = ""
                    if linha["facilidade"] is None:
                        linha["facilidade"] = ""
                    escritor.writerow(linha)
        except OSError as erro:
            print(f"[ERRO] Não foi possível exportar o CSV: {erro}")
            return False
        print(f"Arquivo gerado: {self.caminho_csv} ({len(self.historico)} atendimentos)")
        return True

    # ----------------------------------------------------- módulo de energia
    def _ler_numero(self, texto, padrao, minimo, maximo, inteiro=False):
        """Lê um número dentro de um intervalo. Enter vazio usa o valor padrão."""
        while True:
            resp = self._entrada(f"{texto} [Enter = {padrao}]: ").replace(",", ".")
            if resp == "":
                return padrao
            try:
                valor = int(resp) if inteiro else float(resp)
            except ValueError:
                print("Digite apenas números.")
                continue
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um valor entre {minimo} e {maximo}.")

    def simular_energia(self):
        """Compara 3 alternativas para o banho quente com os dados do usuário."""
        if self.dados_energia is None:
            print("O módulo de energia não está disponível (dados não carregados).")
            return
        dados = self.dados_energia
        padrao = energia.cenario_padrao(dados)
        print("\n--- SIMULAÇÃO DE ENERGIA: BANHO QUENTE ---")
        print("Pressione Enter para usar o valor sugerido. Não digite dados pessoais.")
        cenario = {
            "moradores": self._ler_numero("Quantas pessoas tomam banho quente por dia", 1, 1, 10, inteiro=True),
            "minutos_banho": self._ler_numero("Minutos de cada banho", padrao["minutos_banho"], 1, 60),
            "potencia_w": self._ler_numero("Potência do chuveiro em watts (etiqueta)", padrao["potencia_w"], 1000, 9000),
            "tarifa_base": self._ler_numero("Tarifa por kWh da sua fatura em R$", padrao["tarifa_base"], 0.1, 3.0),
        }
        print("Bandeira tarifária do mês: " + ", ".join(f"{i + 1}={b}" for i, b in enumerate(energia.BANDEIRAS)))
        indice = int(self._ler_opcao("Escolha a bandeira (1 a 4): ", ["1", "2", "3", "4"]))
        cenario["bandeira"] = energia.BANDEIRAS[indice - 1]
        cenario["imovel_proprio"] = self._ler_sn("O imóvel é seu (não é alugado)? (s/n): ")

        resultados = energia.comparar(cenario, dados)
        print(f"\nPeríodo comparado: 1 mês (30 dias). Tarifa usada: R$ {energia.tarifa_efetiva(cenario['tarifa_base'], cenario['bandeira'], dados):.4f}/kWh")
        for r in resultados:
            print(f"\n{r['nome']}")
            print(f"  Consumo da rede: {r['kwh_rede_mes']:.1f} kWh/mês | Custo: R$ {r['custo_mes']:.2f}/mês")
            if r["tipo"] != "referência":
                print(f"  Economia estimada: R$ {r['economia_mes']:.2f}/mês (R$ {r['economia_ano']:.2f}/ano)")
                print(f"  CO2 evitado: {r['co2_evitado_kg_ano']:.1f} kg/ano")
            if r["investimento"] > 0:
                print(f"  Investimento: R$ {r['investimento']:.2f}", end="")
                if r["payback_meses"] is not None:
                    print(f" | Retorno: {r['payback_meses'] / 12:.1f} anos")
                else:
                    print(" | Sem retorno calculável")
            print(f"  Viabilidade: {r['viabilidade']}")
            for obs in r["observacoes"]:
                print(f"  * {obs}")
        print("\nRecomendação:")
        for linha in energia.recomendar(resultados, cenario, dados):
            print(f"  {linha}")
        print("\nAviso: são estimativas com premissas em data/energia_dados.json, não garantias.")
        print("Para o consumo real, veja a sua fatura e a etiqueta do aparelho.")
