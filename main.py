from flask import Flask, request, jsonify #flask, e um micro framewrok, utilizado no desenvolvimento web, atravez dele vou criar a api
from flask_basicauth import BasicAuth #biblioteca responsavel por protege a API de acessos nao desejado, vai pedir uma autenticacao basica para so depois poder acessa a API
from sklearn.utils import resample
from textblob import TextBlob #biblioteca capaz de fazer analise em liguagem natural ou seja normal
from sklearn.linear_model import LinearRegression
import pickle # serializacao

modelo = pickle.load(open('modelo.sav', 'rb')) #pickle e responsavel pelo processo de serializacao, grava e ler variaveis em arquivo, a variavel gravada e um modelo ja treinado, agora estamos lendo, para gravar usar o dump, para ler o load
colunas = ['tamanho', 'ano', 'garagem']

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'julio' #Name e senha para poder acessar a API
app.config['BASIC_AUTH_PASSWORD'] = 'alura'

basic_auth = BasicAuth(app) #A biblioteca vai passar no app e garanti que so seja feito o acesso da API passando pela autenticacao basica

@app.route('/') # A rota, '/' é a rota base(home)
def home():
    return 'Minha primeira API.'

@app.route('/sentimento/<frase>') #<frase> o usuario vai passar uma varivel atravez da url, atravez dessa tag<>   
@basic_auth.required #Esse endpoint so pode ser acessado se for passado a autenticacao correta
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to = 'en') #para para o ingles pq o algoritmo tem um desempenho bem melhor nesse idioma
    polaridade = tb_en.sentiment.polarity #analisa se a fazer é positiva ou negatica, sendo 1 positiva e - 1 negatica
    return "polaridade: {}" .format(polaridade)

@app.route('/cotacao/', methods = ['POST']) #A chama agora nao é mais GET e sim POST, o POST foi projetado para aceita os dados anexados no corpo da mensagem de requisição para armazenamento...
@basic_auth.required
def cotacao():
    dados = request.get_json() #vai pegar os valores recebidos json e colocar na variavel dados
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco = preco[0]) #no desenvolvimento o web o formato json é frequentimente usado entao é bom a gente devolver o resultado em json 

app.run(debug = True) #debug vai fazer com que flask restart a aplicaçao quando alguma alteraçao for feita