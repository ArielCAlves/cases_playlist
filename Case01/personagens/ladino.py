from personagens.base import Personagem
from random import randint

class Ladino(Personagem):
    def __init__(self, nome):
        super().__init__(nome, "Ladino")

    def atacar(self, inimigo):
        dano = randint(1, self.agilidade * 2)
        inimigo.vida -= dano
        print(f"{self.nome} atacou {inimigo.nome} furtivamente com suas adagas venenosas e causou {dano} de dano!")
        
    def usar_habilidade(self, inimigo):
        custo_mana = 5
        if self.mana >= custo_mana:
            self.mana -= custo_mana
            dano = randint(1, self.energia * 1)
            inimigo.vida -= dano
            print(f"{self.nome} usou caminho das sombras e o {inimigo.nome} ficou um pouco confuso, casou {dano} de dano!")
        else:
            print("Mana insuficiente para usar habilidade!")