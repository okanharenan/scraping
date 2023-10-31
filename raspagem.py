import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

#raspagem de dados
url = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"# url para raspagem

# Cabeçalho personalizado para solicitações
headers= {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
 
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content,'html.parser')
qtd_itens = soup.find('div',id='listingCount').get_text().strip()

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]
print(qtd)

ultima_pagina = math.ceil(int(qtd)/20)

# Coleta os dados de todas as páginas
dic_produto = { 'marca':[],'preco':[] } 
for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content,'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        #dic_produto.append(marca,preco)

        dic_produto['marca'].append(marca)
        dic_produto['preco'].append(preco)

# Cria um DataFrame
df = pd.DataFrame(dic_produto)

# Salva os dados em um arquivo CSV
df.to_csv(r'C:\Users\USER\Desktop\Web-Scriph.csv', encoding='utf-8', sep=';')
        