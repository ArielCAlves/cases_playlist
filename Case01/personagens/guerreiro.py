from personagens.base import Personagem
from random import randint

class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, "Guerreiro")

    def atacar(self, inimigo):
        dano = randint(1, self.forca * 2)
        inimigo.vida -= dano
        print(f"{self.nome} atacou {inimigo.nome} com seu imenso machado e causou {dano} de dano!")
        
    def usar_habilidade(self, inimigo):
        custo_mana = 5
        if self.mana >= custo_mana:
            self.mana -= custo_mana
            dano = randint(1, self.energia * 1)
            inimigo.vida -= dano
            print(f"{self.nome} usou alguma skill do machado {inimigo.nome} e causou {dano} de dano!")
        else:
            print("Mana insuficiente para usar habilidade!")