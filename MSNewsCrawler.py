import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
import csv
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
from google.colab import files #importei esse pacote para fazer o download do arquivo JSON gerado
import matplotlib.pyplot as plt #é a biblioteca responsavel por criar grafico.
from datetime import datetime

# Alguns sites utilizam CAPTCHAs, firewalls (como Cloudflare) e técnicas de impressão digital para bloquear robôs e evitar acessos automatizados. Essas estratégias, conhecidas como mitigação de bots, aanti-raspagem oulimitação de taxa nos obrigou a fazer subistituição do site "https://pebmed.com.br/" para o site "https://pt.euronews.com/saude/noticias-de-saude"

# dados de entrada
#https://pt.euronews.com/saude/noticias-de-saude
#https://www.saude.gov.br
#https://www.gov.br/saude/pt-br

requisicaoDePagina = requests.get('https://www.saude.gov.br')

conteudo = requisicaoDePagina.content

#mostra o tipo Pyhton da página
print(type(conteudo))
#joga para a variável site todo o conteúdo da página passada pelo requests.get()
site = BeautifulSoup(conteudo, 'html.parser')

#imprime o site inteiro, como o original
print(site)

#joga para a variável noticias todos os elementos "article", que é onde está cada uma das manchetes do site princial
noticias = site.findAll("div")

#imprime tipo Python de noticias
print(type(noticias))
print(noticias)
#cria uma variável do tipo lista para guardar os dados em um JSON
resposta = []
#cria uma variável para numerar as noticias
noticia_nr = 1
titN = 0
ondN = 0
resN = 0
subN = 0
imgN = 0

#faz um laço na lista noticias (no plural), atribuindo cada item da lista para a variável noticia (no singular)
for noticia in noticias:
    agora = datetime.now() #serve para pegar a data e a hora atual
    data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
    tit = ""
    subt = ""
    res = ""
    ond = ""
    im = ""

    #encontra nas tags do HTMO título, resumo e onde está publicada cada uma das noticias, e joga para as respectivas variáveis
    titulo = noticia.find("h1")
    subtitulo = noticia.find("h2")
    resumo = noticia.find("p")
    onde = noticia.find("a")
    img = noticia.find("img")

    if(titulo):
        #joga o texto de cada uma das tags
        tit = titulo.text
        print("Título:", tit)
        titN += 1
    if(subtitulo):
        #como pode não haver resumo em algumas notícias, é feito um teste.
        subt = subtitulo.text
        print("Subtitulo:", subt)
        subN += 1
    if(onde):
        ond = onde.get('href')
        print("Onde:", ond)
        ondN += 1
    if(resumo):
        #como pode não haver resumo em algumas notícias, é feito um teste.
        res = resumo.text
        print("Resumo:", res)
        resN += 1
    if(img):
        #como pode não haver resumo em algumas notícias, é feito um teste.
        im =  img.get('src')
        print("Imagem:", im)
        imgN += 1
        #um print para separa as noticias
        print("....")
        # Cria uma espécie de dicionario para depois jogar para o JSON
        dados = {'NUMERO': str(noticia_nr), 'TITULO': tit, 'SUBTITULO': subt, 'RESUMO': res, 'ONDE': ond, 'IMAGEM':im, 'DATA': str(data_formatada)}

        # Pendura o dicionario em uma lista e incrementa a variável que conta o número de noticias
        resposta.append(dados)
        noticia_nr += 1

#final do laço que percorre a lista de notícias
#apenas dois prints para mostrar o tipo da resposta e a resposta transformada em string
print("Tipo da resposta", type(resposta))
print(resposta)



# Converte os objetos Pyhton em objeto JSON e exporta para o noticias.json
with open('noticias.json', 'w') as arquivo:
    arquivo.write(str(json.dumps(resposta, indent=4)))


# Link para download do arquivo JSON usando a bib do Python
#FileLink("noticias.json")

#faz o download usando a boblioteca do Colab
files.download('noticias.json')


print("Data e hora formatada:", data_formatada)
# Dados
categorias = ['TITULO', 'SUBTITULO', 'ONDE', 'RESUMO', 'ÍMAGEM']
valores = [titN, subN, ondN ,resN, imgN]

# Criando o gráfico de barras
plt.bar(categorias, valores, linewidth=0.5, width=0.6, color=[ 'green', 'blue', 'yellow','red','aqua'])

# Adicionando rótulos e título
plt.xlabel('Categorias', fontsize=12, fontweight='bold')
plt.ylabel('Valores')
plt.title('Gráfico de Barras total da pesquisa')

# Ajustando os limites do eixo y para melhor visualização
plt.ylim(0, max(valores) + 5)

# Exibindo o gráfico
plt.show()