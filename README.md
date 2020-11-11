# Análise de poluentes atmosféricos

Este é um projeto que eu fiz envolvendo análise de poluentes atmosféricos pelos dados fornecidos pela [CETESB](https://cetesb.sp.gov.br/) (Companhia Ambiental do Estado de São Paulo) através do sistema [QUALAR](https://qualar.cetesb.sp.gov.br/qualar/home.do). É feita a coleta dos dados através de web scrapping, a visualização através do matplotlib e o treinamento de um modelo de aprendizado de máquina com [TensorFlow](https://www.tensorflow.org/?hl=pt-br).

## Coleta dos dados
A coleta dos dados é feita através do script **coleta.py**. Para a realização da coleta, é necessário se registrar no sistema [QUALAR](https://qualar.cetesb.sp.gov.br/qualar/home.do). Após o registro, basta alterar os valores das chaves no dicionário *login* para as suas respectivas credenciais:

```python
login = {
  "cetesb_login": "SEU_LOGIN_AQUI",
  "cetesb_password": "SUA_SENHA_AQUI"
}
```
Após isso basta alterar as variáveis *ano* e *medida* de acordo com o desejado. Há uma lista das medidas possíveis para consulta na docstring da função *consulta*.
Ao fim da consulta será salvo um .csv na pasta "dados" com nome referente ao ano e à medida.

## Visualização e modelagem
No notebook **visual.ipynb** são feitos o treinamento da rede neural e a visualização dos dados em série temporal. É necessário ter o TensorFlow instalado em sua máquina para a execução do notebook, mas também é possível executá-lo através do [Google Colab](https://colab.research.google.com/drive/1gQVuP9wJXyjfGMSsdn9wCxhMAJ2CYXJ0?usp=sharing) se você não tiver (ainda estou fazendo alterações no código para utilizar os .csv deste repo).
