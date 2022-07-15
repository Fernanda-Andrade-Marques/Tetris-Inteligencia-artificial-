import tetris_ia.alggene as alggene
import tetris_ia.tetris_jogo as game
import tetris_ia.tetris_ia as ia
import tetris_ia.analisador as analisador
import matplotlib.pyplot as plt
import argparse, copy

def main(no_show_game):

    # Configurações do jogo
    VELOCIDADE_JOGO= 100
    NUM_GER        = 100
    NUM_POP        = 15
    NUM_EXP        = 10
    VAO           = 0.3
    NUM_FILHO      = round(NUM_POP*VAO)
    TAXA_MUTACAO  = 0.2
    TAXA_CROSSOVER = 0.75

    #alguma variáveis/dados
    experimentos = []
    init_pop    = alggene.algortimoGenetico(NUM_POP) #população inicial

    for e in range(NUM_EXP): #Copia o número da população inicial para fazer experimentos 
        pop         = copy.deepcopy(init_pop)
        geracoes = [] #Começa a lista de gerações

        for g in range(NUM_GER):
            geracoes.append(copy.deepcopy(pop))#salva a geração dos experimentos

            selected_pop = pop.selection(pop.cromossomos, NUM_FILHO)#aqui vai escolher os cromossomos 
            novo_cromo   = pop.operador(selected_pop, crossover="uniforme", mutacao="aleatorio", taxa_crossover=TAXA_CROSSOVER, taxa_mutacao=TAXA_MUTACAO) #Aplica a mutação/crossover

            for i in range(NUM_FILHO):
                estado_jogo = ia.rodar_jogo(pop.cromossomo[i], VELOCIDADE_JOGO, no_show_game) #Vai rodar o jogo para cada um dos cromossomos
                novo_cromo[i].conta_aptidao(estado_jogo) #Calculando a aptidão

            pop.substituir(novo_cromo) #Os novos filhos que foram gerados são acrescentados na população
            aptidao = [cromo.pontuacao for chrom in pop.cromossomo]
            print(aptidao) #printa a aptidão
            print(pop) #printa a população

        experimentos.append(geracoes) #salva o progresso dos experimentos

    an = analisador.analisador(experimentos)# Analisa o progresso do experimento

    return an.pesos #retorna o melhor cromossomo de cada geração/experimento

if __name__ == "__main__":
    
    analisadora = argparse.ArgumentParser(description="Tetris IA") # Definindo as possibilidades do comandno argparse
    analisadora.add_argument('--train',action='store_true',help='Whether or not to train the AI')
    analisadora.add_argument('--game',action='store_true',help='Run the base game without AI')
    analisadora.add_argument('--no-show',action='store_true',help='Whether to show the game')

    args = analisadora.parse_args()

    if (args.train):
       
        melhor_cromos = main(args.no_show) #ensina a INTELIGENCIA ARTIFICIAL e logo após executa com o cromossomo que ela escolheu
    
    else:
        #Roda o jogo com os pesos das pontuações informados
        otimo_peso = [-0.97, 5.47, -13.74, -0.73,  7.99, -0.86, -0.72]
        cromo = alggene.cromossomo(otimo_peso)
        ia.rodar_jogo(cromo, velocidade=100, no_show=False)