import pygame
import random
import numpy as np
import copy
import tetris_ia.tetris_jogo as game
import tetris_ia.tetris_ia as ia


class cromossomo():
    def __init__(self, pesos):
        self.pesos = pesos
        self.pontuacao   = 0

    def conta_aptidao(self, estado_jogo): #Calcula aptidão
        self.pontuacao = estado_jogo[2]

    def conta_melhor_mov(self, quadro, peca, mostrar_jogo = False): #Calcula o melhor movimento, seleciona o melhor movimento baseado no peso do cromossomo.
        
        melhor_pos_x = 0 # Melhor posição em X
        melhor_pos_y = 0 # Melhor posição em Y
        melhor_rot   = 0 # Melhor rotação
        melhor_pontuacao = -100000 # Melhor pontuação

       
        num_buracos_antes, num_blocos_bloqueio_antes = game.conta_info_mov_inicial(quadro) #  Faz a conta do total de buracos e peças acima dos buracos antes de escolher a posição
        for r in range(len(game.PECAS[peca['forma']])):#Fazer todas rotações posiveis
            for x in range(-2,game.QUADROLARGURA-2):#Fazer em torno de todas posições posiveis
                mov_info = game.conta_mov_info(quadro, peca, x, r,num_buracos_antes , num_blocos_bloqueio_antes, )
               
                if (mov_info[0]): # Verificar se o movimento é válido
                    mov_pontuacao = 0 # Calcula a pontuacao do movimento
                    for i in range(1, len(mov_info)):
                        mov_pontuacao += self.pesos[i-1]*mov_info[i]
                   
                    if (mov_pontuacao > melhor_pontuacao): #Atualiza melhor movimento
                        melhor_pontuacao = mov_pontuacao
                        melhor_pos_x = x
                        melhor_rot = r
                        melhor_pos_y = peca['y']

        if (mostrar_jogo):
            peca['y'] = melhor_pos_y
        else:
            peca['y'] = -2

        peca['x'] = melhor_pos_x
        peca['rotacao'] = melhor_rot

        return melhor_pos_x, melhor_rot

class algortimoGenetico:
    def __init__ (self, num_pop, num_pesos=7, lb=-1, ub=1):
        self.cromossomos = []

        for i in range(num_pop):
            pesos = np.aleatorio.uniforme(lb, ub, tamanho =(num_pesos))
            cromo = cromossomo(pesos)
            self.cromossomos.append(cromo)

            estado_jogo = ia.rodar_jogo(self.cromossomo[i], 1000, 200000, True) # Avaliar a apitidão
            self.cromossomos[i].conta_aptidao(estado_jogo)
            
    def operator(self, mutacao="uniforme", taxa_crossover=0.5, taxa_mutacao=0.1): #Define o operador genético que vai usar
       
        novo_cromo = self._aritmetico_crossover(cromossomo, mutacao,  taxa_crossover, taxa_mutacao) #faz crossover
        self.mutacao(novo_cromo, mutacao, taxa_mutacao)#faz mutação

        return novo_cromo


    def substituir(self, novo_cromo): # Troca os cromossomos da população pelos novos cromossomos

        new_pop = sorted(self.cromossomos, key=lambda x: x.pontuacao, reverse=True)
        new_pop[-(len(novo_cromo)):] = novo_cromo
        random.shuffle(new_pop)

        self.cromossomos = new_pop    

    def _aritmetico_crossover(self, selected_pop, taxa_crossover=0.4):#gera outro cromossomo utilizando o crossover genetico
        N_genes    = len(selected_pop[0].pesos) #tamanho cromossomo
        novo_cromo = [copy.deepcopy(c) for c in selected_pop]#

        for i in range(0, len(selected_pop), 2):
            a = random.random()
            #Seleciona um valor qualquer para cada pai e faz a comparação entre eles e a taxa de cruzamento, se os dois forem menores que a taxa acontecerá um cruzamento, se forem maiores os pais entram na nova população.
            tc_pai_1 = random.randint(0,100)
            tc_pai_2 = random.randint(0,100)
            if ( tc_pai_1 < taxa_crossover*100 and tc_pai_2 < taxa_crossover*100):
                try:
                    for j in range(0, N_genes):
                        novo_cromo[i].pesos[j]   = a*novo_cromo[i].pesos[j] + (1 - a)*novo_cromo[i+1].pesos[j]
                        novo_cromo[i+1].pesos[j] = a*novo_cromo[i+1].pesos[j]  + (1 - a)*novo_cromo[i].pesos[j]

                except IndexError:
                    pass

        return novo_cromo

    def mutacao(self, cromossomos, type, taxa_mutacao):#escolhe o tipo de mutação
        
        if (type == "aleatorio"):
            self._rand_mutacao(cromossomos, taxa_mutacao)
        else:
            raise ValueError("Tipo {type} não definido")

    def _rand_mutacao(self, cromossomo, taxa_mutacao): #Faz a mutação de certo cromossomo usando mutação aleatória

        for cromo in cromossomo:
            for i, point in enumerate(cromo.pesos):
                if random.random() < taxa_mutacao:
                    cromo.pesos[i] = random.uniforme(-1.0, 1.0)