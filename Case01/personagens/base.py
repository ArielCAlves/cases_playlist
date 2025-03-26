class Personagem:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.level = 1
        self.pontos_disponiveis = 10
        self.forca = 1
        self.vitalidade = 1
        self.energia = 1
        self.agilidade = 1
        self.vida = 1
        self.mana = 1

    def apresentar(self):
        print(f"Você é {self.nome}, um(a) {self.classe} corajoso(a) em busca de aventuras!\n")

    def distribuir_pontos(self):
        print(f"\nNível: {self.level}")
        print(f"Pontos disponíveis: {self.pontos_disponiveis}")
        print("Distribua seus pontos nos atributos:")

        while self.pontos_disponiveis > 0:
            print(f"Força: {self.forca}, Vitalidade: {self.vitalidade}, Energia: {self.energia}, Agilidade: {self.agilidade}")
            atributo = int(input("Qual atributo deseja aumentar?\n1) Força\n2) Vitalidade\n3) Energia\n4) Agilidade\n"))

            if atributo in [1, 2, 3, 4]:
                pontos = int(input("Quantos pontos deseja adicionar a este atributo?\n "))            
                if pontos <= self.pontos_disponiveis and pontos + self.forca + self.vitalidade + self.energia + self.agilidade <= 14:
                    if atributo == 1:
                        self.forca += pontos
                    elif atributo == 2:
                        self.vitalidade += pontos
                    elif atributo == 3:
                        self.energia += pontos
                    elif atributo == 4:
                        self.agilidade += pontos

                    self.pontos_disponiveis -= pontos
                else:
                    print("Você não pode distribuir mais pontos que 10 pontos.\n")
            else:
                print("Atributo inválido.\n")

        self.vida = 5 * self.vitalidade
        self.mana = 5 * self.energia