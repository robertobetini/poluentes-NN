import requests
import pandas as pd
import os

from auxiliar import splitHTMLTables

def consulta(login: dict, ano: int, medida: str, estacao="270"):
  '''
  O login deve ser feito na forma de dicionário:
  login = {
    "cetesb_login": "seu_usuario",
    "cetesb_password": "sua_senha"
  }
  Realiza consultas nos anos desejados, colocados em uma lista de ints, e sobre as medidas
  desejadas (temperatura, concentração de poluentes, partículas, etc.), colocadas em uma 
  lista de strings.
  Por padrão, a estação selecionada é a Marg. Tietê - Pte Remédios.
  As medidas podem ser:
  "CO" - monóxido de carbono
  "DV" - direção do vento
  "DVG" - direção do vento global 
  "ERT" - enxofre reduzido total 
  "MP10" - material particulado < 10 um 
  "MP2.5" - material particulado < 2.5 um 
  "NO" - monóxido de nitrogênio
  "NO2" - dióxido de nitrogênio
  "NOX" - óxidos de nitrogênio (NO + NO2)
  "O3" - ozônio
  "PRESS" - pressão atmosférica
  "RADG" - radiação solar global
  "RADUV" - radiação ultra-violeta
  "SO2" - dióxido de enxofre
  "TEMP" - temperatura do ar
  "UR" - umidade relativa do ar
  "VV" - velocidade do vento
  '''

  # Dicionário pra traduzir a medida desejada para o valor do input html
  medida_para_numero = {
    "CO": "16",
    "DV": "23",
    "DVG": "21",
    "ERT": "19",
    "MP10": "12",
    "MP2.5": "57",
    "NO": "17",
    "NO2": "15",
    "NOX": "18",
    "O3": "63", 
    "PRESS": "29",
    "RADG": "26",
    "RADUV": "56",
    "SO2": "13",
    "TEMP": "25",
    "UR": "28",
    "VV": "24"
  }

  #Verificamos se existem valores de ano inválidos
  if type(ano) != int:
    print(f'{ano} não é um valor do tipo INT. Cancelando consulta.')
    return

  # Verificando se existem valores invalidos em medidas
  if medida.upper() not in medida_para_numero:
    print(f'{medida} não é um valor válido para medida. Consulte os valores válidos na docstring.')
    return
  
  # Se não existe a pasta /dados/, ela é criada
  try:
    os.mkdir(f'{os.getcwd()}\\dados')
  except:
    print('Pasta de dados: ', f'{os.getcwd()}\\dados')
    pass
  
  path = f'{os.getcwd()}\\dados\\{medida}_{ano}.csv'

  # Verificando se essa consulta já foi realizada:
  try:
    open(path, 'x')
  except:
    print(f'Consulta para {medida} em {ano} já foi realizada!')
    return

  # O requests.Session nos livra da necessidade de ficar passando cookies a cada requisição,
  # ele faz isso automaticamente
  session = requests.Session()

  # Acessamos a página com o formulário do Qualar através de uma requisição GET
  print('Fazendo login...')
  s = session.get('https://qualar.cetesb.sp.gov.br/qualar/home.do')
  if s.status_code != 200:
    print('Falha na validação. Confira as informações de login.')
    print(f'STATUS CODE: {s.status_code}')
    return

  # Então precisamos preencher o formulário com as informações de login.
  # Para isso é preciso criar um dicionário com o login e senha.
  # Para saber facilmente quais são os valores das chaves do dicionário, é recomendável que
  # se utilize a ferramenta inspecão do seu browser. Precisamos dos valores de input id dos
  # campos de login e senha (neste caso são, respectivamente, cetesb_login e cetesb_password)
  # O formulário será enviado para um url específico para ser validado, e podemos encontrá-lo
  # inspecionando o botão de 'submit' do formulário.

  url_autenticador = 'https://qualar.cetesb.sp.gov.br/qualar/autenticador'

  # O formulário é enviado com uma requisição POST
  s = session.post(url_autenticador, data=login)

  # Agora sim, finalmente, fazemos a busca dos dados.
  # Podemos descobrir os valores de cada campo e de cada seletor pela ferramenta de inspeção
  # do browser.
  url_dados = 'https://qualar.cetesb.sp.gov.br/qualar/exportaDados.do'
  payload = {"method": "pesquisar"}
  query = {
    "irede": "A",
    "dataInicialStr": f"01/01/{ano}",
    "dataFinalStr": f"31/12/{ano}",
    "cDadosInvalidos": "",
    "iTipoDado": "P",
    "estacaoVO.nestcaMonto": estacao,
    "parametroVO.nparmt": medida_para_numero[medida]
  }
  print(f'Fazendo consulta para valores de {medida} em {ano}.')
  s = session.post(url_dados, data=query, params=payload)
  tabelas = splitHTMLTables(s.text)

  # Para alguns parâmetros a pesquisa pode não retornar resultado algum, por isso
  # fazemos esse teste
  try:
    dados = pd.read_html(tabelas[1])[0] # A segunda tabela contém os dados de interesse
    dados = dados[[4, 5, 9, 10]] # Selecionando as colunas de interesse
    #print(dados)
    dados.columns = ['Data', 'Hora', 'Unidade de medida', 'Media horaria'] # E renomeamos

    # Por fim, salvamos os dados como um arquivo .csv:
    print(f'Salvando os dados em {path}.')
    dados.to_csv(path, index=False)
  except:
    print('Não foram encontrados dados para os parâmetros fornecidos.')
    os.remove(path)
  finally:
    print('Finalizando consulta.')



############# JAMAIS DIVULGUE SUAS INFORMAÇÕES PESSOAIS DE LOGIN #############
login = {
  "cetesb_login": "SEU_LOGIN_AQUI",
  "cetesb_password": "SUA_SENHA_AQUI"
}
############# JAMAIS DIVULGUE SUAS INFORMAÇÕES PESSOAIS DE LOGIN #############

ano = 2001
medida = "TEMP"
consulta(login, ano, medida)