import random, time, pygame, sys
from pygame.locals import *

# Configuração de tempo
FREQMOVLADOS = 0.15
FREQMOVBAIXO    = 0.1

# Configuração tela
FPS          = 25
JANELALARGURA = 650
JANELAALTURA = 650
TAMANHOBOX      = 25
QUADROLARGURA   = 10
QUADROALTURA  = 25
VAZIO       = '.'
XMARGEM      = int((JANELALARGURA - QUADROLARGURA * TAMANHOBOX) / 2)
TOPMARGEM    = JANELAALTURA - (QUADROALTURA * TAMANHOBOX) - 5



# CORES
BRANCO      = (255, 255, 255)
CINZA    = (185, 185, 185)
PRETO       = (  0,   0,   0)
VERMELHO         = (155,   0,   0)
LUZVERMELHA    = (175,  20,  20)
VERDE       = (  0, 155,   0)
LUZVERDE  = ( 20, 175,  20)
AZUL      = (  0,   0, 155)
LUZAZUL   = ( 20,  20, 175)
AMARELO      = (155, 155,   0)
LUZAMARELA = (175, 175,  20)

BORDACOR =     VERMELHO
BGCOR        = BRANCO
TEXTOCOR       = PRETO
CORES          = (    AZUL,     VERDE,     VERMELHO,    AMARELO)
CORESLUZ     = (LUZAZUL, LUZVERDE, LUZVERMELHA, LUZAMARELA)

assert len(CORES) == len(CORESLUZ)

# Aqui iremos definir os modelos(formas) das peças
# Modelos de peças
# os modelos definem o tamanho de cada linha e a coluna para a rotação de cada peça
MODELOLARGURA  = 4 
MODELOALTURA = 4

S_MODELO_PECA = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_MODELO_PECA = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_MODELO_PECA = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_MODELO_PECA = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_MODELO_PECA= [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_MODELO_PECA = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_MODELO_PECA = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PECAS = {'S': S_MODELO_PECA,
          'Z': Z_MODELO_PECA,
          'J': J_MODELO_PECA,
          'L': L_MODELO_PECA,
          'I': I_MODELO_PECA,
          'O': O_MODELO_PECA,
          'T': T_MODELO_PECA}

# Definindo se o manual do jogo
MANUAL_jogo = False

#jogo principal
def main():
    global FPSTEMPO, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()

    FPSTEMPO   = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((JANELAALTURA, JANELALARGURA))
    BASICFONT   = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT     = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris com IA') # Nome que plota na bar

    if (MANUAL_jogo):
        rodar_jogo()

def rodar_jogo():
    # variaveis
    ultm_movbaixo_tempo = time.time()
    ultm_movlado_tempo = time.time()
    ultimo_tempo_caida  = time.time()
    quadro = obter_branco()
#considerando que não tem movimento das peças

    mov_baixo  = False 
    mov_esquerda  = False
    mov_direita = False
    pontuacao = 0
    nivel, freqqueda  = calcnivel_freqqueda(pontuacao)
    peca_caindo  = obter_nova_peca()
    nova_peca =  obter_nova_peca()

    while True:
        # Repetição no jogo
        if (peca_caindo == None):
            #nenhuma peça caindo no jogo, temos que colocar uma nova peça
            peca_caindo = nova_peca
            nova_peca = obter_nova_peca()
            pontuacao += 1

            # Reset ultimo tempo de queda
            ultimo_tempo_caida = time.time()

            if (not posicao_valida(quadro, peca_caindo)):
                # Perdeu o jogo
                #  Acabou o espaço para colocar peças novas, então acabou o jogo.
                return

        # verificar para sair
     #   verificar_sair()
        rodar_jogo()
        
        for event in pygame.event.get():
        
                if (event.key == K_LEFT or event.key == K_a):
                    mov_esquerda = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    mov_direita = False
                elif (event.key == K_DOWN or event.key == K_s):
                    mov_baixo = False

        if event.type == KEYDOWN:
                # Movimentando a peça para o lado
                #esquerda
                if (event.key == K_LEFT or event.key == K_a) and posicao_valida(quadro, peca_caindo, adj_X=-1): 

                    peca_caindo['x'] -= 1
                    mov_esquerda         = True
                    mov_direita        = False
                    ultm_movlado_tempo  = time.time()
                #direita
                elif (event.key == K_RIGHT or event.key == K_d) and posicao_valida(quadro, peca_caindo, adj_X=1):

                    peca_caindo['x'] += 1
                    mov_esquerda        = True
                    mov_direita        = False
                    ultm_movlado_tempo  = time.time()

                # Girando a peça
                elif (event.key == K_UP or event.key == K_w):
                    peca_caindo['rotacao'] = (peca_caindo['rotacao'] + 1) % len(PECAS[peca_caindo['forma']])

                    if (not posicao_valida(quadro, peca_caindo)):
                        peca_caindo['rotacao'] = (peca_caindo['rotacao'] - 1) % len(PECAS[peca_caindo['forma']])

                elif (event.key == K_q):
                    peca_caindo['rotacao'] = (peca_caindo['rotacao'] - 1) % len(PECAS[peca_caindo['forma']])

                    if (not posicao_valida (quadro, peca_caindo)):
                        peca_caindo['rotacao'] = (peca_caindo['rotacao'] + 1) % len(PECAS[peca_caindo['forma']])

            # Peça desce mais rapida com a tecla para baixo
                elif (event.key == K_DOWN or event.key == K_s):
                    mov_baixo = True

                    if (posicao_valida(quadro, peca_caindo, adj_Y=1)):
                        peca_caindo['y'] += 1

                    ultm_movbaixo_tempo = time.time()

                elif event.key == K_SPACE:
                    mov_baixo  = False
                    mov_esquerda  = False
                    mov_direita = False

                    for i in range(1, QUADROALTURA):
                        if (not posicao_valida(quadro, peca_caindo, adj_Y=i)):
                            break

                    peca_caindo['y'] += i - 1

        # Movimenta a peça dependendo do que o usuario clica
        if (mov_esquerda or mov_direita) and time.time() - ultm_movlado_tempo > FREQMOVLADOS:
            if mov_esquerda and posicao_valida(quadro, peca_caindo, adj_X=-1):
                peca_caindo['x'] -= 1
            elif mov_direita and posicao_valida(quadro, peca_caindo, adj_X=1):
                peca_caindo['x'] += 1

            ultm_movlado_tempo = time.time()

        if mov_baixo and time.time() - ultm_movbaixo_tempo > FREQMOVBAIXO and posicao_valida(quadro, peca_caindo, adj_Y=1):
            peca_caindo['y'] += 1
            ultm_movbaixo_tempo = time.time()
        # Deixar a peça cair 
        if time.time() - ultimo_tempo_caida > freqqueda:
            # vendo se a peça caiu mesmo
            if (not posicao_valida(quadro, peca_caindo, adj_Y=1)):
                # colocando a peça que caiu na tela
                add_quadro(quadro, peca_caindo)
                num_linhas_removidas = apagar_linha_completa(quadro)

                # Pontuação Bônus
                # 1   pontos para 1 linha
                # 5   pontos para 2 linhas
                # 10  pontos para 3 linhas
                # 20  pontos para 4 linhas
                num_linhas_removidas = apagar_linha_completa(quadro)
                if(num_linhas_removidas == 1):
                    pontuacao += 1
                
                elif (num_linhas_removidas == 2):
                    pontuacao += 5
                   
                elif (num_linhas_removidas == 3):
                    pontuacao += 10
                  
                elif (num_linhas_removidas == 4):
                    pontuacao += 20
                nivel, freqqueda = calcnivel_freqqueda(pontuacao)
                peca_caindo = None
            else:
         
                peca_caindo['y'] += 1
                peca_caindo      = time.time()

        # Desenhando tudo na tela
        DISPLAYSURF.fill(BGCOR)
        desenhar_quadro(quadro)
        desenhar_status(pontuacao, nivel)
        desenhar_nova_peca(nova_peca)

        if peca_caindo != None:
            desenha_peca(peca_caindo)

        pygame.display.update()
        FPSTEMPO.tick(FPS)

#funções jogo

def check_key_pressiona():
 # Percorrer a fila de eventos procurando um evento KEYUP e remover os eventos KEYDOWN
    verificar_sair()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def fazer_obj_texto(text, font, color):
    surf = font.render(text, True, color)

    return surf, surf.get_rect()

def verificar_sair():
    for event in pygame.event.get(): 
        rodar_jogo()

def mostrar_tela_texto(text):
   # Mostra um texto grande no meio da tela ate que pressionem uma tecla
   
    title_surf, title_rect = fazer_obj_texto(text, BIGFONT, )
    title_rect.center      = (int(JANELALARGURA / 2), int(JANELAALTURA / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    # Desenhe o texto
    title_surf, title_rect = fazer_obj_texto(text, BIGFONT, TEXTOCOR)
    title_rect.center      = (int(JANELALARGURA / 2) - 3, int(JANELALARGURA / 2) - 3)
    DISPLAYSURF.blit(title_surf, title_rect)

    # Desenhe o adicional "Pressione uma tecla para jogar." texto.
    press_key_surf, press_key_rect = fazer_obj_texto('Pressione uma tecla para começar.', BASICFONT, TEXTOCOR)
    press_key_rect.center = (int(JANELALARGURA / 2), int(JANELAALTURA / 2) + 100)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)

    while check_key_pressiona() == None:
        pygame.display.update()
        FPSTEMPO.tick()


def calcnivel_freqqueda(pontuacao):
    # Calcular o nível e frequência de queda com base na pontuação, retornando o nível
    # em que o jogador está e quantos segundos se passam até que uma peça caindo cai um espaço


    nivel     = int(pontuacao / 400) + 1
    freqqueda = 0.27 - (nivel * 0.02)

    if (not MANUAL_jogo):
        freqqueda = 0.00

    return nivel, freqqueda


def obter_branco():
    #Criar e retornar uma nova estrutura de nova estrutura de dados de quadro em branco

    quadro = []
    for i in range(QUADROLARGURA):
        quadro.append([VAZIO] * QUADROALTURA)

    return quadro

def add_quadro(quadro, peca):
    for x in range(MODELOLARGURA):
        for y in range(MODELOALTURA):
            if PECAS[peca['forma']][peca['rotacao']][y][x] != VAZIO:
                quadro[x + peca['x']][y + peca['y']] = peca['color']

def posicao_valida(quadro, peca, adj_X=0, adj_Y=0):
    #Retorna Verdadeiro se a peça estiver dentro do tabuleiro e não colidir

    for x in range(MODELOLARGURA):
        for y in range(MODELOALTURA):
            is_above_board = y + peca['y'] + adj_Y < 0

            if is_above_board or PECAS[peca['forma']][peca['rotacao']][y][x] == VAZIO:
                continue

            if not esta_quadro(x + peca['x'] + adj_X, y + peca['y'] + adj_Y):
                return False

            if quadro[x + peca['x'] + adj_X][y + peca['y'] + adj_Y] != VAZIO:
                return False

    return True

def obter_nova_peca():
    #Retornar uma peça nova aleatória em uma rotação e cor aleatórias 

    forma     = random.choice(list(PECAS.keys()))
    nova_peca = {'forma': forma,
                'rotacao': random.randint(0, len(PECAS[forma]) - 1),
                'x': int(QUADROLARGURA / 2) - int(MODELOLARGURA / 2),
                'y': -2, 
                'color': random.randint(0, len(CORES)-1)}

    return nova_peca

def esta_quadro(x, y):
    #Verificar se a peça está no tabuleiro

    return x >= 0 and x < QUADROLARGURA and y < QUADROALTURA

#vai ver se tem linha completa, se tiver retorna true
def linha_completa(quadro, y):
    for x in range(QUADROLARGURA):
        if quadro[x][y] == VAZIO:
            return False

    return True

def conv_to_pixels_coords(boxx, boxy):

    return (XMARGEM + (boxx * TAMANHOBOX)), (TOPMARGEM + (boxy * TAMANHOBOX))


def apagar_linha_completa(quadro):
    num_apagar_linha= 0
    y = QUADROALTURA - 1    
    while y >= 0:
        if linha_completa(quadro, y):
            for demolirY in range(y, 0, -1):
                for x in range(QUADROLARGURA):
                    quadro[x][demolirY] = quadro[x][demolirY-1]

            for x in range(QUADROLARGURA):
                quadro[x][0] = VAZIO

            num_apagar_linha += 1
        else:
            y -= 1  

    return num_apagar_linha


def desenhar_box(boxx, boxy, cor, pixelx=None, pixely=None):

    if cor == VAZIO:
        return

    if pixelx == None and pixely == None:
        pixelx, pixely = conv_to_pixels_coords(boxx, boxy)

    pygame.draw.rect(DISPLAYSURF, CORES[cor], (pixelx + 1, pixely + 1, TAMANHOBOX - 1, TAMANHOBOX - 1))
    pygame.draw.rect(DISPLAYSURF, CORESLUZ[cor], (pixelx + 1, pixely + 1, TAMANHOBOX - 4, TAMANHOBOX - 4))

#desenhar status do jogo
def desenhar_status(pontuacao, nivel):
  
    score_surf = BASICFONT.render('Pontuação: %s' % pontuacao, True, TEXTOCOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (JANELALARGURA - 150, 80)
    DISPLAYSURF.blit(score_surf, score_rect)

def desenhar_quadro(quadro):

    pygame.draw.rect(DISPLAYSURF, BORDACOR, (XMARGEM - 3, TOPMARGEM - 7, (QUADROLARGURA * TAMANHOBOX) + 8, (QUADROALTURA * TAMANHOBOX) + 8), 5)

    pygame.draw.rect(DISPLAYSURF, BGCOR, (XMARGEM, TOPMARGEM, TAMANHOBOX * QUADROLARGURA, TAMANHOBOX * QUADROALTURA))

    for x in range(QUADROLARGURA):
        for y in range(QUADROALTURA):
            desenhar_box(x, y, quadro[x][y])


def desenha_peca(peca, pixelx=None, pixely=None):

    shape_to_draw = PECAS[peca['forma']][peca['rotacao']]

    if pixelx == None and pixely == None:
  
        pixelx, pixely = conv_to_pixels_coords(peca['x'], peca['y'])

    for x in range(MODELOLARGURA):
        for y in range(MODELOLARGURA):
            if shape_to_draw[y][x] != VAZIO:
                desenhar_box(None, None, peca['color'], pixelx + (x * TAMANHOBOX), pixely + (y * TAMANHOBOX))


def desenhar_nova_peca(peca):

    next_surf = BASICFONT.render('Proxima peça:', True, TEXTOCOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (JANELALARGURA- 150, 130)
    DISPLAYSURF.blit(next_surf, next_rect)

    desenha_peca(peca, pixelx=JANELALARGURA-150, pixely=180)


# Funções de estatísticas do jogo


def conta_mov_info(quadro, peca, x, r, total_buraco_bef, blocos_bloqueio_total_bef):

    peca['rotacao'] = r
    peca['y']        = 0
    peca['x']        = x

    if (not posicao_valida(quadro, peca)):
        return [False]

    # Desce a peca enquanto é uma posição válida
    while posicao_valida(quadro, peca, adj_X=0, adj_Y=1):
        peca['y']+=1

    # Criando um quadro hipotético
    novo_quadro = obter_branco()
    for x2 in range(QUADROLARGURA):
        for y in range(QUADROALTURA):
            novo_quadro[x2][y] = quadro[x2][y]

    # adicionar nova peça no quadro
    add_quadro(novo_quadro, peca)

  # Calcular os lados em contato
    pecas_tamanho, chao_tamanho, lado_paredes = calc_lados_contato(quadro, peca)

    # Calculando linhas apagadas
    num_apagar_linhas = apagar_linha_completa(novo_quadro)

    blocos_bloqueio_total = 0
    total_buracos          = 0
    max_altura           = 0

    for x2 in range(0, QUADROLARGURA):
        b = calc_heuristica(novo_quadro, x2)
        total_buracos += b[0]
        blocos_bloqueio_total += b[1]
        max_altura += b[2]

    novos_buracos           = total_buracos - total_buraco_bef
    novos_blocos_bloqueio = blocos_bloqueio_total - blocos_bloqueio_total

    return [True, max_altura, num_apagar_linhas, novos_buracos, novos_blocos_bloqueio, pecas_tamanho, chao_tamanho, lado_paredes]

def conta_info_mov_inicial(quadro):
    total_furos          = 0
    blocos_bloqueio_total = 0

    for x2 in range(0, QUADROLARGURA):
        b = calc_heuristica(quadro, x2)

        total_furos          += b[0]
        blocos_bloqueio_total += b[1]

    return total_furos, blocos_bloqueio_total

def calc_heuristica(quadro, x):
    
  #  As heurísticas são compostas por: número de buracos, número de blocos acima
   # furo e altura máxima.
    total_buracos        = 0
    local_buracos       = 0
    bloco_acima_buraco = 0
    tem_buraco      = False
    soma_alturas        = 0

    for y in range(QUADROALTURA-1, -1,-1):
        if quadro[x][y] == VAZIO:
            local_buracos += 1
        else:
            soma_alturas += QUADROALTURA-y

            if local_buracos > 0:
                total_buracos += local_buracos
                local_buracos = 0

            if total_buracos > 0:
                bloco_acima_buraco+= 1

    return total_buracos, bloco_acima_buraco, soma_alturas

def calc_lados_contato(quadro, peca):

    peca_tamanho = 0
    chao_tamanho = 0
    lado_paredes  = 0

    for Px in range(MODELOLARGURA):
        for Py in range(MODELOALTURA):

            # Wall
            if not PECAS[peca['forma']][peca['rotacao']][Py][Px] == VAZIO: # Quadrante faz parte da peça
                if peca['x']+Px == 0 or peca['x']+Px == QUADROLARGURA-1:
                    lado_paredes += 1

                if peca['y']+Py == QUADROALTURA-1:
                    chao_tamanho += 1
                else:
                # Para outras opecas no contorno do template:
                    if Py == MODELOALTURA-1 and not quadro[peca['x']+Px][peca['y']+Py+1] == VAZIO:
                        peca_tamanho += 1

                #os extremos do template sao colorido: confere se ha pecas do lado deles
                if Px == 0 and peca['x']+Px > 0 and not quadro[peca['x']+Px-1][peca['y']+Py] == VAZIO:
                        peca_tamanho += 1

                if Px == MODELOLARGURA-1 and peca['x']+Px < QUADROLARGURA -1 and not quadro[peca['x']+Px+1] [peca['y']+Py] == VAZIO:
                        peca_tamanho+= 1

            # Outras peças
            elif peca['x']+Px < QUADROLARGURA and peca['x']+Px >= 0 and peca['y']+Py < QUADROALTURA and not quadro[peca['x']+Px][peca['y']+Py] == VAZIO:  #quadrante do tabuleiro colorido mas nao do template

                # O quadrante vazio do template esta colorido no tabuleiro
                if not PECAS[peca['forma']][peca['rotacao']][Py-1][Px] == VAZIO:
                    peca_tamanho += 1

                if Px > 0 and not PECAS[peca['forma']][peca['rotacao']][Py][Px-1] == VAZIO:
                    peca_tamanho += 1

                if Px < MODELOLARGURA-1 and not PECAS[peca['forma']][peca['rotacao']][Py][Px+1] == VAZIO:
                    peca_tamanho += 1

                    #(nao pode haver pecas em cima)

    return  peca_tamanho, chao_tamanho, lado_paredes