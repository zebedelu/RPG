import os, time, random, keyboard, colorama

colorama.init()

class Inimigo():
    def __init__(self, nome, vida: int, defesa: int, equipamento: dict, nivel: int, posicao: list):
        self.nome = nome
        self.vida = vida
        self.defesa = defesa
        self.equipamento = equipamento # ex: ["espada", 30]
        self.nivel = nivel
        self.vida_max = vida

        posicao = [posicao[0]+1, posicao[1]+1]
        self.position = [posicao[0], posicao[1]]
        if not mapa[posicao[1]][posicao[0]] in colisiveis:
            mapa[posicao[1]][posicao[0]] = "i"

    def dano(self, dano):
        if dano >= self.defesa:
            self.vida -= (dano - self.defesa)
        else:
            self.vida -= (dano/self.vida_max)*self.defesa

        self.vida = int(self.vida)
        if self.vida <= 0:
            mapa[self.position[1]][self.position[0]] = " "
            print("")
            print("Nivel: +1")
            print("Sua vida se restaurou!")
            input("O inimigo morreu!")
            personagem.defesa += self.defesa//2
            personagem.nivel += 1
            personagem.vida = personagem.vida_max
            return 0

class Personagem():
    def __init__(self, nome, vida: int, defesa: int, equipamento: dict, inventory: list, nivel: int, nome_classe: str, dano_a_mais: int, posicao=None):
        self.nome = nome
        self.vida = vida

        self.arma_equipada = equipamento # ex: ["espada": 30]
        self.dano_a_mais = dano_a_mais

        self.defesa = defesa
        self.nivel = nivel

        self.inventory = inventory
        self.inventory.append(self.arma_equipada)

        self.classe = nome_classe
        self.vida_max = vida
        
        # Se for encontrado no mapa, algum valor com a letra "p" represetando o jogador
        # a variavel position terá o valor da posição dele no mapa
        for ny, linha_y in enumerate(mapa):
            for nx, linha_x in enumerate(linha_y):
                if linha_x == "p":
                    posicao = [nx, ny]
                    break

        self.position = [posicao[0], posicao[1]]
        if not mapa[posicao[1]][posicao[0]] in colisiveis:
            mapa[posicao[1]][posicao[0]] = "p"

    def dano(self, dano: int):
        if dano >= self.defesa:
            self.vida -= (dano - self.defesa)
        else:
            self.vida -= (dano/self.vida_max)*self.defesa
        
        self.vida = int(self.vida)
        if self.vida <= 0:
            print()
            while True:
                print('''\n\n\n
  ________                        ________                     
 /  _____/_____    _____   ____   \_____  \___  __ ___________ 
/   \  ___\__  \  /     \_/ __ \   /   |   \  \/ _/ __ \_  __ \\
\    \_\  \/ __ \|  Y Y  \  ___/  /    |    \   /\  ___/|  | \/
 \______  (____  |__|_|  /\___  > \_______  /\_/  \___  |__|   
        \/     \/      \/     \/          \/          \/       \n\n\n
''')
                input("TECLE ENTER PARA FECHAR.")
                quit()

    def cura(self, cura: int):
        if self.vida+cura <= self.vida_max:
            self.vida += cura
        elif self.vida+cura > self.vida_max:
            self.vida = self.vida_max

    def mover_player(self, moverxy):
        player_y = 0
        player_x = 0 
        for n, v in enumerate(mapa):
            if v.count("p") == 1:
                player_y = n
                player_x = v.index("p")

        mover_para = mapa[player_y+moverxy[1]][player_x+moverxy[0]]
        if not mover_para in colisiveis:
            #posição antiga do player
            mapa[player_y][player_x] = " "
            mapa[player_y+moverxy[1]][player_x+moverxy[0]] = "p"
            self.posicao = [player_y+moverxy[1],player_x+moverxy[0]]

        return [mover_para, [player_x+moverxy[0], player_y+moverxy[1]]]

    def show_map_of_player(self):
        global configs
        player_y = 0
        player_x = 0
        for n, v in enumerate(mapa):
            if v.count("p") == 1:
                player_y = n
                player_x = v.index("p")
        
        mapa_player = []
        escala_y = configs["escala_y"]
        escala_x = configs["escala_x"]
        for y in range(player_y - escala_y, player_y + escala_y +1):
            mapa_player.append([])
            for x in range(player_x - escala_x, player_x + escala_x +1):
                parte_do_mapa = "v"
                try:
                    if (x >= 0) and (y >= 0):
                        parte_do_mapa = mapa[y][x]
                except:
                    pass

                mapa_player[-1].append(parte_do_mapa)

        return mapa_player
    
class Batalha():
    def __init__(self, player, inimigo):
        self.jogador = player
        self.inimigo = inimigo
        self.chance_fugir = random.randint(0,100)

    def atacar(self):
        while not keyboard.is_pressed("enter"): 1
        time.sleep(0.2)

        show_mapa(self.jogador.show_map_of_player(), True, "Sua hora de atacar.")
        print("Segure ENTER para definir o dano.")
        print("")

        playerdano = 0
        while True:
            playerdano = self.jogador.arma_equipada[1] + random.randint(-10,10) + self.jogador.dano_a_mais
            if playerdano < 0:
                playerdano = 1
            print(playerdano, end="\r")
            time.sleep(0.3)
            if keyboard.is_pressed("enter"): break
            time.sleep(0.3)
            if keyboard.is_pressed("enter"): break
            #não foi usado o for com 3 loops nessa parte, porque o break não iria fazer efeito dentro do loop while
            #iria fazer efeito dentro do for, deixando-o em loop infinitamente

        self.inimigo.dano(playerdano)
        return playerdano

    def inimigo_atacar(self):
        inidado = self.inimigo.equipamento[1] + random.randint(-10,10)
        self.jogador.dano(inidado)
        return inidado
    
    def item(self):
        show_mapa(self.jogador.show_map_of_player(), True)
        print("Qual item deseja usar:")

        index = 0

        itens_usaveis_do_inv = []
        for n, v in enumerate(self.jogador.inventory):
            # se o item for usavel, será mostrado para o jogador para ele poder usar em batalha
            if v[0] in itens_usaveis[0]:
                print(f'({index+1}) {v[0]}: {v[1]}')
                itens_usaveis_do_inv.append([v[0],v[1]])
                index += 1

        choice = input(" > : ")

        if choice.isdigit() and len(itens_usaveis_do_inv) >= int(choice) > 0:
            choice = int(choice)-1
            self.jogador.cura(itens_usaveis_do_inv[choice][1])
            self.jogador.inventory.remove(itens_usaveis_do_inv[choice])
            input("Vez do inimigo!")
        else:
            return 0
    
    def fugir(self):
        show_mapa(self.jogador.show_map_of_player(), True, colorama.Fore.LIGHTGREEN_EX+"Você tenta fugir."+colorama.Fore.RESET)
        print("Tem certeza que deseja TENTAR fugir? (chance de sucesso: "+str(self.chance_fugir)+")")
        print("(1) Não.")
        print("(2) Sim.")

        choice = ""
        while True:
            choice = input(" > : ")
            if choice.isdigit() and int(choice) in [1,2]:
                choice = int(choice)
                break
        
        if choice == 2 and self.chance_fugir >= random.randint(0,100):
            return 2
        elif choice == 2:
            return 1
        return 0
    
    def chose_option(self):
        show_mapa(self.jogador.show_map_of_player(), True, f"{colorama.Fore.LIGHTRED_EX}{self.inimigo.nome} te ataca!{colorama.Fore.RESET}\n{colorama.Fore.LIGHTBLUE_EX}Oque você faz?{colorama.Fore.RESET}")
        while True:
            msg = ""
            if self.inimigo.vida <= 0:
                break

            atack = True
            print("Sua vida:",f"{self.jogador.vida}/{self.jogador.vida_max}")
            print(colorama.Fore.RED)
            print("#"*self.jogador.vida, end=colorama.Fore.LIGHTBLACK_EX)
            print("#"*(self.jogador.vida_max-self.jogador.vida), end=colorama.Fore.RESET)
            print()
            print(f"Vida do {self.inimigo.nome}:",f"{self.inimigo.vida}/{self.inimigo.vida_max}","\tnivel:",self.inimigo.nivel,"\tdefesa:",self.inimigo.defesa)
            print(colorama.Fore.RED)
            print("#"*self.inimigo.vida, end=colorama.Fore.LIGHTBLACK_EX)
            print("#"*(self.inimigo.vida_max-self.inimigo.vida), end=colorama.Fore.RESET)
            print()
            print()
            print(" "*25,end="")
            print(f"{'(1) LUTAR': <30}", end="")
            print(f"{'(2) ITEM': <30}", end="")
            print(f"{'(3) FUGIR': <30}")
            print()

            while True:
                keyboard.press_and_release('ctrl+backspace')
                choice = input(" > : ")
                if choice.isdigit() and 1 <= int(choice) <= 3:
                    choice = int(choice)
                    break
            
            cor = colorama.Fore.CYAN
            reset = colorama.Fore.RESET

            if choice == 1:
                msg = cor+f"Você ataca!{reset}\n"
                msg += cor+f"Você deu: {batalha.atacar()} de dano{reset}"
            if choice == 2:
                _ = batalha.item()
                if _ == 0:
                    atack = False
            elif choice == 3:
                _ = batalha.fugir()
                if _ == 2:
                    msg = f"{colorama.Fore.LIGHTGREEN_EX}Você consegue escapar!{colorama.Fore.RESET}"
                    print("Você consegue escapar!")
                    return "fuga"
                elif _ == 0:
                    atack = False

            if atack and self.inimigo.vida > 0:
                msg += f"\n{cor}Ele ataca!{reset}\n"
                msg += f"{cor}Ele deu: {batalha.inimigo_atacar()} de dano{reset}"

            show_mapa(self.jogador.show_map_of_player(), True, msg)
        return "vitoria"
    
class Bau():
    def __init__(self, posicao, jogador):
        itens_bau = [
            "pocao de cura",
            "espada",
            "machado",
            "comida",
        ]
        self.item = [random.choice(itens_bau), random.randint(20,50)] # item & nivel de efeito
        self.posicao = [posicao[0]+1, posicao[1]+1]
        self.jogador = jogador
        mapa[self.posicao[1]][self.posicao[0]] = "b"

    def abrir(self):
        self.jogador.inventory.append(self.item)
        mapa[self.posicao[1]][self.posicao[0]] = " "

        # loop para ver qual das ferramentas é mais forte, e equipa-la no jogador automaticamente
        maior = 0
        item_mais_forte = []
        for n, v in enumerate(self.jogador.inventory):
            if v[0] in itens_usaveis[1]:
                if v[1] > maior:
                    maior = v[1]
                    item_mais_forte = v

        self.jogador.arma_equipada = item_mais_forte

        return self.item
    
def show_mapa(mapa_cenario, limparconsole, mensagem_personalizada=""):
    global cenario_objs_letra
    os.system(clear*int(limparconsole))
    print("-"*120)
    amplificacao = configs["amplificacao"]

    for numero1, valor_y in enumerate(mapa_cenario):
        linha_x = ""
        for numero2, valor_x in enumerate(valor_y):
            letra_anterior = valor_y[numero2-1]
            
            if valor_x in list(cenario_objs_letra.keys()):
                letra = cenario_objs_letra[valor_x]
                sombra = letra

                if letra_anterior == " ":
                    if type(letra) == type(""):
                        sombra = colorama.Fore.LIGHTBLACK_EX+letra+colorama.Fore.RESET
                    if type(letra) == type([]):
                        sombra = []
                        for let in letra:
                            sombra.append(colorama.Fore.LIGHTBLACK_EX+let+colorama.Fore.RESET)

                if type(letra) == type([]):
                    linha_x += random.choice(sombra)
                    for i in range((((amplificacao+int(amplificacao*1.1))))-1):
                        linha_x += random.choice(letra)
                elif type(letra) == type(""):
                    linha_x += sombra+(letra*((amplificacao+int(amplificacao*1.1))-1))
            else:
                # se existir algum elemento desconhecido no cenário, ele irá imprimir "?" no lugar do objeto normal
                linha_x += colorama.Fore.MAGENTA+"?"+colorama.Fore.BLACK+("?"*((amplificacao+int(amplificacao*1.1))-1))

        linha_x += "|"
        linha_x = "|" + linha_x

        atributo_lado = [
            [],
            [colorama.Fore.CYAN, "Nome: ",personagem.nome, colorama.Fore.RESET],
            [colorama.Fore.MAGENTA, "Classe: ",personagem.classe, colorama.Fore.RESET],
            [colorama.Fore.YELLOW, "Nível: ",personagem.nivel, colorama.Fore.RESET],
            [colorama.Fore.RED, "HP: ",personagem.vida, colorama.Fore.RESET],
            [colorama.Fore.LIGHTMAGENTA_EX, "Defesa: ", personagem.defesa, colorama.Fore.RESET],
            [],
            ["Inventory:"],
            [],
            ["Item Equipado:"],
            [],
            ["Oque aconteceu antes:"]
        ]+mensagem_personalizada.split("\n")
        
        for item in personagem.inventory:
            inventory_index = atributo_lado.index(["Inventory:"])
            atributo_lado.insert(inventory_index+1, ["\t",item[0]+": ",item[1]])

        inventory_index = atributo_lado.index(["Item Equipado:"])
        atributo_lado.insert(inventory_index+1, ["\t",personagem.arma_equipada[0],": ",personagem.arma_equipada[1]])
        
        for i in range(amplificacao):
            linha_y_index = i+numero1*3
            endprint = "\n"
            for n, item in enumerate(atributo_lado):
                if n == linha_y_index:
                    endprint = "".join(list(map(str, item)))+"\n"

            print(linha_x, end=endprint)

    print("-"*120)

def configurations(clearconsole=True):
    global configs
    os.system(clear*int(clearconsole))
    
    print("(0) Sair das configurações.")
    print("(1) Editar Escala em X:", configs["escala_x"])
    print("(2) Editar Escala em Y:", configs["escala_y"])
    print("(3) Editar Tamanho da Imagem:", configs["amplificacao"])

    while True:
        valor = input("Insira a opção para editar: ")
        if valor.isdigit():
            valor = int(valor)
            break
        else:
            print("Insira uma opção válida.")

    while True:
        if valor == 0: break
        editar = input("Insira um valor: ")
        if editar.isdigit():
            editar = int(editar)
            break
        else:
            print("Insira uma opção válida.")

    if valor == 0: return
    if valor == 1: configs["escala_x"] = editar
    if valor == 2: configs["escala_y"] = editar
    if valor == 3: configs["amplificacao"] = editar

# mensagem de clear que irá ser usada
clear = ""
# dependendo de qual não der erro, será usada a que der certo no sistema
if os.system("cls") == 0: clear = "cls"
elif os.system("clear") == 0: clear = "clear"
os.system(clear)

configs = {
    "escala_y": 3,
    "escala_x": 7,
    "amplificacao": 3
}

'''
espaço em branco: nada.
p: player ou jogador.
v: void, vazio fora do mapa.
m: muralha/parede.
i: inimigo. 
'''
mapa = [
    ["m","m","m","m","m","m","m"," "," "," "," "," "," "],
    ["m"," "," ","m"," "," ","m"," ","m","m","m","m"," "],
    ["m"," "," ","m"," "," ","m"," "," "," "," ","m","m"],
    ["m"," ","m","m","m"," ","m","m","m","m"," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," ","m"," "],
    [" "," "," "," "," "," "," ","m","m","m"," ","m"," "],
    [" "," "," "," "," "," "," "," "," ","m"," ","m"," "],
    [" "," "," "," "," "," "," "," "," ","m"," ","m"," "],
    [" "," "," "," "," "," "," "," "," ","m","m","m","m"],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["m","m","m"," "," "," ","m","m","m","m","m"," "," "],
    [" "," ","m"," "," "," ","m"," "," "," ","m"," "," "],
    [" "," ","m"," "," "," ","m"," "," "," ","m"," "," "],
    [" "," ","m","m"," ","m","m"," "," "," ","m","m","m"],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," ","p"," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "," "," "," "]
]
cenario_objs_letra = {
    "p":["O","P"],
    " ":" ",
    "v":"|",
    "m":["H","M"],
    "i":["/","\\"],
    "b":[".",","]
}

# Sistema de Void
mapa.append(list("v"*len(mapa[0])))
mapa.insert(0,list("v"*len(mapa[0])))
for n in range(len(mapa)):
    mapa[n].append("v")
    mapa[n].insert(0,"v")

# coisas que não se podem atravessar no cenário, ou que tem algum efeito ao colidir.
colisiveis = [
    "m",
    "v",
    "i",
    "b"
]
movs = {
    "w":[0,-1],
    "a":[-1,0],
    "s":[0,1],
    "d":[1,0],
}
itens_usaveis = [
    [ # itens de cura
        "pocao de cura",
        "comida"
    ],
    [ # itens de dano
        "espada",
        "machado"
    ]
]
classes_disponiveis = {
    "humano":{"vida":100, "+arma_dano": 0, "defesa":0, "arma":["espada", 30], "inventario":[["comida",30],["comida",35]]},
    "golem":{"vida":115, "+arma_dano": -10, "defesa": 20, "arma":["espada", 15], "inventario":[["comida",40],["pocao de cura",60],["pocao de cura",60]]},
    "mago":{"vida":70, "+arma_dano": 20, "defesa":-5, "arma":["espada", 30], "inventario":[["pocao de cura",10],["pocao de cura", 20]]}
}

print("recomendado colocar em janela maximizada.")
if input("ENTER para continuar, 0 para sair.\n") == "0": quit()

while True:
    nome = input("Insira seu nome para o jogador: ").capitalize()
    if nome != "" and not nome.isspace():
        break
    os.system(clear)
    print("Porfavor, insira um nome não-vazio.")
os.system(clear)
print()

while True:
    for n, v in enumerate(classes_disponiveis):
        print(f"({n+1}) {v}:\n\
            vida: "+str(classes_disponiveis[v]["vida"])+"\n\
            dano a mais na arma: "+str(classes_disponiveis[v]["+arma_dano"])+"\n\
            defesa: "+str(classes_disponiveis[v]["defesa"]))

    classe = input("Insira sua classe para o jogador: ")
    os.system(clear)
    if classe.isdigit() and 0 < int(classe) <= len(classes_disponiveis):
        classe = list(classes_disponiveis.keys())[int(classe)-1]
        break
    elif classe == "" or classe.isspace():
        print("Insira alguma opção válida.")
os.system(clear)
print()

nivel = input("Insira seu nivel (padrão: 1, máximo: 5, minimo: 1): ")
if nivel.isdigit() and 1 <= int(nivel) <= 5:
    nivel = int(nivel)
else:
    print("Valor inválido, será reposto pelo valor padrão: ")
    nivel = 1
os.system(clear)
print()

# Para efeito de animação
for n in "Para começar, tecle W, A, S ou D.":
    print(n,end="",flush=True)
    time.sleep(0.01)

personagem = Personagem(nome=nome,
                        vida=classes_disponiveis[classe]["vida"],
                        defesa=classes_disponiveis[classe]["defesa"],
                        equipamento=classes_disponiveis[classe]["arma"],
                        inventory=classes_disponiveis[classe]["inventario"],
                        dano_a_mais=classes_disponiveis[classe]["+arma_dano"],
                        nivel=nivel,
                        nome_classe=classe)

inimigos = []
inimigos.append(Inimigo(nome="Guardião", vida=115, defesa=7, nivel=1, posicao=[1,3], equipamento=["machado", 30]))
inimigos.append(Inimigo(nome="Mago", vida=100, defesa=5, nivel=3, posicao=[4, 9], equipamento=["machado",25]))
inimigos.append(Inimigo(nome="Goblin", vida=100, defesa=5, nivel=3, posicao=[7, 4], equipamento=["machado",25]))

baus = []
baus.append(Bau([1,1],personagem))
baus.append(Bau([1,7],personagem))
baus.append(Bau([12,12],personagem))

msg_personalizada = ""
keys = ["'","e","w","a","s","d"]

while True:
    event = keyboard.read_event(suppress=False)

    # tecla_pressionada irá armazenar o valor da tecla que foi pressionada, e os ifs a seguir iram verificar qual que foi a tecla
    tecla_pressionada = ""
    if event.event_type == keyboard.KEY_DOWN:
        if event.name in keys:
            tecla_pressionada = event.name

    if tecla_pressionada != "":
        colisão = " "

        if keyboard.is_pressed("'"):
            keyboard.press_and_release('ctrl+backspace')
            configurations()
        elif keyboard.is_pressed("e"):
            keyboard.press_and_release('ctrl+backspace')
            if len(personagem.inventory) >= 2:
                print(f"Insira o número do item que deseja remover (Não é possivel remover itens equipados: {personagem.arma_equipada[0]}: {personagem.arma_equipada[1]}): ")
                for n, v in enumerate(personagem.inventory):
                    print(f"({n+1}) {v[0]}: {v[1]}")

                choice = input(" > : ")
                
                if choice.isdigit() and len(personagem.inventory) >= int(choice) > 0 and personagem.inventory[int(choice)-1] != personagem.arma_equipada:
                    choice = int(choice)-1
                    try:
                        msg_personalizada = "Você jogou fora "+str(personagem.inventory[choice][0])
                        del personagem.inventory[choice]
                    except:
                        print("Número fora de lista.")
        
        movimento = [0,0]
        if tecla_pressionada == "w": movimento = movs["w"]
        elif tecla_pressionada == "a": movimento = movs["a"]
        elif tecla_pressionada == "s": movimento = movs["s"]
        elif tecla_pressionada == "d": movimento = movs["d"]

        if movimento != [0,0]:
            try:
                keyboard.press_and_release('ctrl+backspace')
                colisão = personagem.mover_player(movimento)
            except:
                pass
                
        if "i" in colisão:
            for inimigo in inimigos:
                if inimigo.position == colisão[1]:
                    batalha = Batalha(personagem, inimigo)
                    ganhou_pelo_oque = batalha.chose_option()
                    if ganhou_pelo_oque == "vitoria":
                        input("Você venceu! (Pressione ENTER)")
                        msg_personalizada = "Inimigo morreu!\nNível: +1\nVida: 100"
                    elif ganhou_pelo_oque == "fuga":
                        msg_personalizada = "Você escapou!"
                    del batalha
                    show_mapa(personagem.show_map_of_player(), True, msg_personalizada)
                    print("W, A, S e D para se mover.")
                    print("E para remover algo do inventário.")
                    print("' para configurações.")
                    break
        if "b" in colisão:
            for bau in baus:
                if bau.posicao == colisão[1]:
                    item_ganho = bau.abrir()

                    msg_personalizada = f"Você ganhou:\n{item_ganho[0]}: {item_ganho[1]}"
                    
                    try:
                        colisão = personagem.mover_player(movimento)[0]
                    except:
                        pass
                    break
            
        if not colisão[0] in colisiveis:
            show_mapa(personagem.show_map_of_player(), True, msg_personalizada)
            print("W, A, S e D para se mover.")
            print("E para remover algo do inventário.")
            print("' para configurações.")

    time.sleep(0.1)