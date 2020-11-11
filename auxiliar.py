def cleanTable(string: str):
  '''
  Esta função serve apenas para trocar as vírgulas dos valores numéricos por pontos e
  remover a linha "Exportar Dados" da tabela gerada pelo Qualar, pois a mera existência 
  dela complica a sua transformação em dataframe do Pandas.
  '''

  newtext = ''
  i = string.find('<tr')
  f = string.find('</tr') + 4
  for n in range(len(string)):
    if i < n < f:
      continue
    elif string[n] == ',':
      newtext += '.'
    else:
      newtext += string[n]
  return newtext

def splitHTMLTables(htmlStr: str, tables=[]) -> list:
  '''
  Recebe uma string de uma página HTML e recorta suas tabelas,
  para facilitar sua transformação em dataframe pelo Pandas.
  '''

  i = htmlStr.find('<table')
  if i < 0:
    return tables
  else:
    f = htmlStr.find('</table')

    # A string "</table>" tem 8 caracteres e ela precisa estar dentro da
    # string adicionada a tables para que ela feche a tag "<table>", por isso
    # a substring é htmlStr[i:f + 8]

    tables.append(htmlStr[i:f + 8])

    # Para prosseguir com a recursão, queremos fatiar a string para que não
    # tenhamos tabelas desnecessariamente duplicadas. Além disso, colocar a mesma string
    # na linha abaixo iria levantar uma exceção de limite máximo de recursão.

    splitHTMLTables(htmlStr[f + 9:], tables=tables) # Passamos as tabelas que já temos
  tables[1] = cleanTable(tables[1])
  return tables