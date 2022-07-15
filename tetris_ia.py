import  time, pygame, sys
from pygame.locals import *
import tetris_ia.tetris_jogo as game

tamanho   = [640, 480] # tamanho da tal
tela = pygame.display.set_mode((tamanho[0], tamanho[1]))

def rodar_jogo(cromossomo, velocidade, pontuacao_max= 20000, no_show = False):

    game.FPS = int(velocidade)
    game.main()
# definindo como vai ficar a tela
    quadro            = game.obter_branco() # deixar a tela preta
    ultimo_tempo_caida= time.time()
    pontuacao          = 0
    nivel, freq_queda = game.calcnivel_freqqueda(pontuacao)
    peca_caindo   = game.obter_nova_peca()
    nova_peca       = game.obter_nova_peca()

    # Calculando o melhor movimento
    cromossomo.conta_melhor_mov(quadro, peca_caindo)

    num_pecas_caidas = 0
    apagar_linhas   = [0,0,0,0] # Combos

    vivo = True
    ganhar  = False

    # Loop do jogo
    while vivo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Jogo encerrado pelo")
                exit()

        if peca_caindo == None:
           #como não tem nenhuma peça caindo, estamos pegando a nova peca e colocando para cair
            peca_caindo = nova_peca
            nova_peca    = game.obter_nova_peca()

            # Decidindo o melhor movimento com base nos seus pesos
            cromossomo.conta_melhor_mov(quadro, peca_caindo, no_show)

            # Atualizando o número de peças usadas e a pontuaçao
            num_pecas_caidas +=1
            pontuacao+= 1

            # Reseta o tempo de caida
            ultimo_tempo_caida = time.time()

            if (not game.posicao_valida(quadro, peca_caindo)):
                # Perdeu o jogo
                # Acabou o espaço para colocar peças novas, então acabou o jogo
                vivo = False

        if no_show or time.time() - ultimo_tempo_caida > freq_queda:
            if (not game.posicao_valida(quadro, peca_caindo, adj_Y=1)):
               #peça esta caindo parou
                game.add_quadro(quadro, peca_caindo)

                num_linhas_removidas = game.apagar_linha_completa(quadro)
                if(num_linhas_removidas == 1):
                    pontuacao += 1
                    apagar_linhas[0] += 1
                elif (num_linhas_removidas == 2):
                    pontuacao += 5
                    apagar_linhas[1] += 1
                elif (num_linhas_removidas == 3):
                    pontuacao += 10
                    apagar_linhas[2] += 1
                elif (num_linhas_removidas == 4):
                    pontuacao+= 20
                    apagar_linhas[3] += 1

                peca_caindo = None
            else:
                # Peça não parou, por isso rodamos
                peca_caindo['y'] += 1
                ultimo_tempo_caida = time.time()

        if (not no_show):
            desenharjogotela(quadro, pontuacao, nivel, nova_peca, peca_caindo, cromossomo)

        # parar a condição
        if (pontuacao > pontuacao_max):
            vivo = False
            ganhar = True

    # Salvar o estado do jogo
    estado_jogo = [num_pecas_caidas, apagar_linhas, pontuacao, ganhar]

    return estado_jogo

def desenharjogotela(quadro, pontuacao , nivel, nova_peca, peca_caindo, cromossomo):
    """Desenhar o jogo na tela"""

    game.DISPLAYSURF.fill(game.BGCOR)
    game.desenhar_quadro(quadro)
    game.desenhar_status(pontuacao, nivel)
    game.desenhar_nova_peca(nova_peca)

    if peca_caindo != None:
        game.desenha_peca(peca_caindo)

    pygame.display.update()
    game.FPSTEMPO.tick(game.FPS)