from random import randint

class Inimigo:
    def __init__(self, nome, vida):
        self.nome = nome
        self.vida = vida

    def atacar(self, personagem):
        dano = randint(1, 5)
        personagem.vida -= dano
        print(f"{self.nome} atacou {personagem.nome} e causou {dano} de dano!")