"""Classe que representa uma orientação verificada da base de conhecimento."""


class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    @classmethod
    def de_dicionario(cls, d):
        """Cria a orientação a partir de um registro do JSON.
        Levanta KeyError/TypeError/ValueError se o registro estiver incompleto."""
        obrigatorios = ["id", "categoria", "titulo", "palavras_chave", "resposta",
                        "documentos", "onde", "fonte", "verificado_em"]
        for campo in obrigatorios:
            if campo not in d:
                raise KeyError(campo)
        if not isinstance(d["palavras_chave"], list) or not d["palavras_chave"]:
            raise ValueError("palavras_chave deve ser uma lista não vazia")
        if not isinstance(d["documentos"], list):
            raise ValueError("documentos deve ser uma lista")
        return cls(int(d["id"]), str(d["categoria"]), str(d["titulo"]),
                   [str(p) for p in d["palavras_chave"]], str(d["resposta"]),
                   [str(x) for x in d["documentos"]], str(d["onde"]),
                   str(d["fonte"]), str(d["verificado_em"]))

    def exibir(self):
        print()
        print("=" * 60)
        print(f"{self.titulo}  [{self.categoria}]")
        print("=" * 60)
        print(self.resposta)
        if self.documentos:
            print("\nO que levar / ter em mãos:")
            for doc in self.documentos:
                print(f"  - {doc}")
        print(f"\nOnde fazer: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("-" * 60)
        print("Aviso: este assistente não é canal oficial. Confirme na fonte acima.")
        print()
