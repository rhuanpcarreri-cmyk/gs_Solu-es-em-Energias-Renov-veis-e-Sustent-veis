"""Base de conhecimento: carrega o JSON e faz a busca por pontuação."""

import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i",
           "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c", "º": " ", "ª": " "}

# Palavras comuns que não ajudam a identificar o assunto (não pontuam no título).
PALAVRAS_COMUNS = {"como", "para", "sobre", "quero", "preciso", "onde", "qual",
                   "quais", "fazer", "faco", "minha", "meus", "minhas", "pelo",
                   "pela", "voce", "tenho", "posso", "quando", "fiz", "dele"}

PONTOS_PALAVRA_CHAVE = 3
PONTOS_TITULO = 1
LIMITE_ALTA = 6
LIMITE_MEDIA = 3
MAX_RESULTADOS = 3  # melhor resultado + até 2 alternativas


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-/\"'":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []
        self._chaves = {}  # id -> palavras-chave normalizadas
        self._titulos = {}  # id -> título normalizado

    def carregar(self):
        """Lê o JSON. Nunca derruba o programa: devolve True/False e avisa o motivo."""
        self.orientacoes = []
        try:
            with open(self.caminho, encoding="utf-8") as arq:
                dados = json.load(arq)
        except FileNotFoundError:
            print(f"[ERRO] Arquivo da base não encontrado: {self.caminho}")
            return False
        except json.JSONDecodeError as erro:
            print(f"[ERRO] O arquivo da base está corrompido (linha {erro.lineno}): {self.caminho}")
            return False
        except OSError as erro:
            print(f"[ERRO] Não foi possível ler a base: {erro}")
            return False

        if not isinstance(dados, list):
            print("[ERRO] A base deve ser uma lista de orientações.")
            return False

        ignoradas = 0
        for item in dados:
            try:
                self.orientacoes.append(Orientacao.de_dicionario(item))
            except (KeyError, TypeError, ValueError, AttributeError):
                ignoradas += 1
        if ignoradas:
            print(f"[AVISO] {ignoradas} orientação(ões) com dados incompletos foram ignoradas.")

        self._chaves = {o.id: [normalizar(p) for p in o.palavras_chave] for o in self.orientacoes}
        self._titulos = {o.id: normalizar(o.titulo) for o in self.orientacoes}
        if not self.orientacoes:
            print("[ERRO] Nenhuma orientação válida foi carregada.")
            return False
        return True

    def categorias(self):
        vistas = []
        for o in self.orientacoes:
            if o.categoria not in vistas:
                vistas.append(o.categoria)
        return vistas

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta):
        """Devolve lista de tuplas (pontos, orientacao), da maior para a menor pontuação.
        +3 por palavra-chave encontrada; +1 por palavra (4+ letras) da pergunta que está no título."""
        texto = normalizar(pergunta)
        palavras = {p for p in texto.split() if len(p) >= 4 and p not in PALAVRAS_COMUNS}
        resultado = []
        for o in self.orientacoes:
            pontos = 0
            for chave in self._chaves[o.id]:
                if chave in texto:
                    pontos += PONTOS_PALAVRA_CHAVE
            titulo = self._titulos[o.id]
            for palavra in palavras:
                if f" {palavra} " in titulo:
                    pontos += PONTOS_TITULO
            if pontos > 0:
                resultado.append((pontos, o))
        resultado.sort(key=lambda par: (-par[0], par[1].id))
        return resultado

    @staticmethod
    def confianca(pontos):
        if pontos >= LIMITE_ALTA:
            return "ALTA"
        if pontos >= LIMITE_MEDIA:
            return "MÉDIA"
        return "NENHUMA"

    def buscar(self, pergunta):
        """Devolve (confianca, lista de até 3 tuplas (pontos, orientacao)).
        Abaixo de 3 pontos a confiança é NENHUMA e a lista vem vazia."""
        pontuadas = self.pontuar(pergunta)
        if not pontuadas:
            return "NENHUMA", []
        nivel = self.confianca(pontuadas[0][0])
        if nivel == "NENHUMA":
            return nivel, []
        # alternativas só entram se também tiverem pelo menos pontuação MÉDIA
        relevantes = [par for par in pontuadas if par[0] >= LIMITE_MEDIA]
        return nivel, relevantes[:MAX_RESULTADOS]
