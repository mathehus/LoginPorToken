import pandas as pd
from flask import Flask, jsonify, request , render_template
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient

#conexão com MongoDB
client = MongoClient("localhost", 27017)
db = client.admin
collection = db['Tokens']


app = Flask(__name__)

### swagger  ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Swagger Cripto",
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



#contruir as funcionalidades
@app.route('/')
def homepage():
    #return render_template("index.html")
    return 'A API está no ar'

@app.route('/pegarvendas')
def pegarvendas():

    tabela = pd.read_csv('tabelaAPI.csv')
    total_vendas = tabela['Vendas'].sum()
    resposta = {
        'total_vendas': total_vendas,
    } 
    return jsonify(resposta) 

@app.route('/PegarToken', methods=['POST'])
def PegarToken():
    _json = request.json
    _login = _json['login']
    _senha = _json['senha']

    buscaLogin = collection.find_one(
        {
            "login": _login,
            "senha": _senha
        }
    )

    if buscaLogin != None :
        return jsonify({'mensagem' : 'Logado com sucesso' , 'username' : _login, "token" : buscaLogin['token']})

    else:
        resp = jsonify({'mensagem' : 'Não autorizado'})
        resp.status_code = 401
        return resp

@app.route('/CriarToken', methods=['POST']) 
def CriarToken():   
    try:
        _json = request.json
        _login = _json['login']
        _senha = _json['senha']

        token = "f9bf78b9a18ce6d46a0cd2b0b86df9da"

        buscaLogin = collection.find_one(
            {
            "login": _login,
            "senha": _senha
            }
        )
        #adsa = collection.find()
        if buscaLogin == None :

            db.Tokens.insert_many(
                [
                    {
                    "token": token,
                    "login": _login,
                    "senha": _senha
                    }
                ]
            )

            resp = jsonify({
                'token' : token,
                'mensagem' : 'Criado Com sucesso'
            })

            return resp
        else:

            resp = jsonify({'mensagem' : 'Login já existe', "token" : token
            })
            return resp

    except:
            resp = jsonify({'mensagem' : 'Token Não foi Criado'})
            resp.status_code = 401
            return resp


#rodar a api
app.run(debug= True, port=8080) 