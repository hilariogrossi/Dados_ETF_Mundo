# Como pegar dados de sites com o Python.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Criando o robô
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.get('https://www.etf.com/etfanalytics/etf-finder')
driver.maximize_window() # Para maximizar a página aberta.

time.sleep(5) # Dando um tempo de 5 segundos para a página abrir por completo.

# Encontrando o elemento no site da exebição de 100 ETF´s por página.
botao_100 = driver.find_element('xpath', '/html/body/div[5]/section/div/div[3]'
                                         '/section/div/div/div/div/div[2]'
                                         '/section[2]/div[2]/section[2]'
                                         '/div[1]/div/div[4]/button/label/span')

time.sleep(5) # Esperar 3 segundos para clicar no botão 100 por página.

botao_100.click() # Acionando o botão para mostrar 100 ETF´s por página.
# Se não funcionar usar esse -> driver.execute_script('arguments[0],click;', botao_100) # Acionando o botão para mostrar 100 ETF´s por página.

# Encontrando o número de páginas a ser escaneado.
numero_paginas = driver.find_element('xpath', '//*[@id="totalPages"]') # Acha o número de páginas.
numero_paginas = numero_paginas.text.replace('of ', '') # retira o of e o espaço depois e deixa somente o número de páginas.
numero_paginas = int(numero_paginas) # Transformando o número de páginas em número inteiro.

# Encontrando as tabelas necessárias por página.
lista_tabela_por_pagina = []
elemento_tabela = driver.find_element('xpath', '//*[@id="finderTable"]')

# Lendo a tabela de ETF´s atráves de um FOR.
for pagina in range(1, numero_paginas + 1):
    html_tabela = elemento_tabela.get_attribute('outerHTML')
    tabela = pd.read_html(str(html_tabela))[0]
    lista_tabela_por_pagina.append(tabela) # Guardando as informações dentro da lista de tabelas.
    botao_avancar_pagina = driver.find_element('xpath', '//*[@id="nextPage"]')
    time.sleep(3)
    botao_avancar_pagina.click()

# Colocando as informações na tabela de cadastro de ETF´s.
tabela_cadastro_etfs = pd.concat(lista_tabela_por_pagina)

# Voltando para primeira página.
formulario_de_voltar_pagina = driver.find_element('xpath', '//*[@id="goToPage"]')
formulario_de_voltar_pagina.clear() # Vai limpar o formulário e espera digitar algo.
formulario_de_voltar_pagina.send_keys('1') # Envia o número 1 para o formulário.
formulario_de_voltar_pagina.send_keys(u'\ue007') # Dar o enter no teclado (Código: u'\ue007')

# Ler a tabela de rentabilidade
botao_mudar_para_performance = driver.find_element(('xpath', '/html/body/div[5]/section/div/div[3]'
                                                        '/section/div/div/div/div/div[2]'
                                                        '/section[2]/div[2]/ul/li[2]/span'))
botao_mudar_para_performance.click()
time.sleep(3)
lista_tabela_por_pagina = []
elemento_tabela = driver.find_element('xpath', '//*[@id="finderTable"]')

# Lendo a tabela de ETF´s atráves de um FOR.
for pagina in range(1, numero_paginas + 1):
    html_tabela = elemento_tabela.get_attribute('outerHTML')
    tabela = pd.read_html(str(html_tabela))[0]
    lista_tabela_por_pagina.append(tabela) # Guardando as informações dentro da lista de tabelas.
    botao_avancar_pagina = driver.find_element('xpath', '//*[@id="nextPage"]')
    time.sleep(3)
    botao_avancar_pagina.click()

# Colocando as informações na tabela de cadastro de ETF´s.
tabela_rentabilidade_etfs = pd.concat(lista_tabela_por_pagina)

# Para fechar o Google Chrome
driver.quit()

# Acessando o Ticker das tabelas
tabela_rentabilidade_etfs = tabela_rentabilidade_etfs.set_index('Ticker')
tabela_rentabilidade_etfs = tabela_rentabilidade_etfs[['1 Year', '3 Years', '5 Years']]

tabela_cadastro_etfs = tabela_cadastro_etfs.set_index('Ticker')

print(tabela_cadastro_etfs)
print(tabela_rentabilidade_etfs)

base_de_dados_final = tabela_cadastro_etfs.join(tabela_rentabilidade_etfs, how = 'inner')
# inner só vai pegar os tickers que existem nas duas tabelas
print(base_de_dados_final)
