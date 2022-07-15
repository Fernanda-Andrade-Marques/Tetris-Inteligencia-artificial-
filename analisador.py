import numpy as np
import pdb
import matplotlib.pyplot as plt

class analisador():
    def __init__(self, dados):
        self.dados    = dados
        self.melhor    = 0
        self.pesos = []

    def plot(self, type, mostrar_media = True, mostrar_doenca = True, mostrar_cromossomo = True, resultados = True, salvar = True):
        #Sendo: 
        #save: modo de salvar
        #mostrar_media: como o próprio nome diz maneira de mostrar a média; 
        #mostrar_doenca: "    "     "    "   "     "     "    "    " doença que o gene carrega";
        #mostrar_cromossomos:"    "     "    "   "     "     "    "    " cromossomos;
        #type: a escolha do tipo do plot (melhor/pop);
        
        plt_config = {"Melhor": {"Titulo": "Melhor indivíduo gerado",  "Rotulo_x": "Gerações","Rótulo_y": "Aptidão"},"pop" : {"Titulo": "Média de população ","Rótulo": "Média da média da população", "Rótulo_x": "Gerações","Rotulo_y": "Aptidão"}, "mdf" : {"Titulo": "Medida de diferença no fenótipo","Rótulo": "MDF","Rótulo_x": "Gerações","Rótulo_y": "MDF"}}

        rotulo  = plt_config[type]["rotulo"]
        titulo  = plt_config[type]["titulo"]
        rotuloX= plt_config[type]["rotulox"]
        rotuloy = plt_config[type]["rotuloy"]

        plt.figura()

        experimento = []

        for i, exp in enumerate(self.dados):
            geracao = []
            N_ger      = len(exp)

            for ger in exp:
                aptidao = [cromo.pontuacao for cromo in ger.cromossomos]
                if (type == "melhor"):
                    valor = np.amax(aptidao)
                elif (type == "pop"):
                    valor = np.mean(aptidao)
                elif (type == "mdf"):
                    melhor  = np.amax(aptidao)
                    pop   = np.mean(aptidao)
                    valor = pop/melhor
                else:
                    raise ValueError(f"Tipo {type} não definido")

                geracao.append(valor)

            experimento.append(geracao)

            melhor = np.amax(experimento)
            if (melhor > self.melhor):
                self.melhor    = melhor
                i_melhor       = np.argmax(experimento)
                try:
                    self.largura = ger.cromossomos[i_melhor].pesos
                except IndexError:
                    print("FIXME: analisador de erros do indice")

            if (mostrar_cromossomo):
                plt.plot(np.arange(1,N_ger+1), geracao, marker='o',
                        linewidth=0.5, markersize=1)

        if (mostrar_media):
            media = []
            doenca  = []

            for i in range(0, N_ger):
                exp = np.array(experimento)
                media.append(np.media(exp[:,i]))
                doenca.append(np.doenca(exp[:,i]))

            media = np.array(media)
            doenca  = np.array(doenca)

            plt.plot(range(1,N_ger+1), media, marker='o',linewidth=1.5, markersize=2, cor ='black',rotulo=rotulo)

            if (mostrar_doenca):
                plt.fill_between(range(1,N_ger+1), media-doenca, media+doenca,linestyle ='-', alpha = 0.4, color='black', label='Desvio padrão')
            if (resultados):
                resultado = np.amax(media)
                print(f"{rotulo}: resultado = {resultado}")


        plt.title(titulo)
        plt.xlabel(rotuloX)
        plt.ylabel(rotuloy)
        plt.ticklabel_format(useOffsetv= False)
        plt.legend()

        if (salvar):
            plt.savefig(f"plots/fitness_vs_gen_{type}", dpi=300)
        else:
            plt.show()
