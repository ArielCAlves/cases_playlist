from eventos.evento import Evento
from personagens.guerreiro import Guerreiro
from personagens.mago import Mago
from personagens.ladino import Ladino
from inimigos.goblin import Inimigo

class Jogo:
    def __init__(self):
        self.eventos = {
            "inicio": Evento("Você é um(a) mercenário(a) que chegou na Cidade de Silverton, uma cidade próspera ameaçada pelo terror de Zanbar Bone. Precisa resgatar alguém. Escolha seu caminho:\n1) Ir pela floresta\n2) Ir pela cidade"),
            "mata": Evento("Você está na mata. O que você quer fazer?\n1) Seguir pela mata\n2) Nadar"),
            "trilha": Evento("Você está na trilha. O que você quer fazer?\n1) Seguir a trilha\n2) Pegar o atalho"),
            "batalha": Evento("Apareceu um Goblin na sua frente!! Prepare-se para a batalha!")
        }

    def jogar(self):
        print("Bem-vindo à aventura!")
        evento_atual = self.eventos["inicio"]
        jogador = self.criar_personagem()
        
        while evento_atual:
            print(evento_atual.descricao)
            opcoes = self.obter_opcoes(evento_atual)
            if not opcoes:
                break
            opcao = input("Escolha uma opção (1 ou 2): ")
            evento_atual = opcoes.get(opcao)
            if evento_atual == self.eventos["batalha"]:
                self.enfrentar_goblin(jogador)
                break

    def criar_personagem(self):
        print("\nCrie o seu personagem:")
        nome_personagem = input("Qual é o nome do seu personagem? ")
        print("\nEscolha uma classe para seu personagem:")
        print("1. Guerreiro")
        print("2. Mago")
        print("3. Ladino")
        classe_personagem = input("Qual é a classe do seu personagem? ")

        while classe_personagem not in ['1', '2', '3']:
            print("Escolha inválida. Tente novamente.")
            classe_personagem = input("Qual é a classe do seu personagem? ")

        if classe_personagem == '1':
            jogador = Guerreiro(nome_personagem)
        elif classe_personagem == '2':
            jogador = Mago(nome_personagem)
        else:
            jogador = Ladino(nome_personagem)

        jogador.distribuir_pontos()
        return jogador

    def obter_opcoes(self, evento):
        opcoes = {}
        if evento == self.eventos["inicio"]:
            opcoes = {
                "1": self.eventos["mata"],
                "2": self.eventos["trilha"]
            }
        elif evento == self.eventos["mata"]:
            opcoes = {
                "1": self.eventos["batalha"],
                "2": self.eventos["batalha"]
            }
        elif evento == self.eventos["trilha"]:
            opcoes = {
                "1": self.eventos["batalha"],
                "2": self.eventos["batalha"]
            }
        return opcoes

    def enfrentar_goblin(self, jogador):
        inimigo = Inimigo("Goblin", 20)
        print(f"Apareceu um Goblin na sua frente!! Prepare-se para a batalha!")
        while jogador.vida > 0 and inimigo.vida > 0:
            print(f"\n{jogador.nome}: Vida: {jogador.vida}, Mana: {jogador.mana}")
            print(f"{inimigo.nome}: Vida: {inimigo.vida}")

            escolha = input("O que você quer fazer? (atacar, usar habilidade) ").lower()
            if escolha == "atacar":
                jogador.atacar(inimigo)
                inimigo.vida = max(0, inimigo.vida)
            elif escolha == "usar habilidade":
                jogador.usar_habilidade(inimigo)   
                inimigo.vida = max(0, inimigo.vida)
            else:
                print("Opção inválida. Tente novamente.")

            if inimigo.vida <= 0:
                print(f"\nVocê derrotou {inimigo.nome}!")
                break

            inimigo.atacar(jogador)

        if jogador.vida <= 0:
            print("GAME OVER!! Você foi derrotado!")
        else:
            print("Parabéns! Você derrotou o Goblin e passou da primeira parte!")
            print("Continuação em breve...")