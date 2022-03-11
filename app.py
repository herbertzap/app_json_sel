from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'bigbuda_herbert_zap'
app.config['MYSQL_PASSWORD'] = '62032597Hz.#'
app.config['MYSQL_DB'] = 'bigbuda_export_json'
#mysql = MySQL(app)




#cors validate dominios o ip
CORS(app,resource={r"/pedidos/*":{"origins":"http://localhost"}})
from pedidos import products

#busqueda@cross_origin
@app.route("/")
def index():
  return render_template('index.html')
    
#ver todos los pedidos exportados
@app.route('/')
def get_pedidos():
    return jsonify({"pedidos": products})

#busqueda por rut de colaborador.
@app.route('/pedidos/<string:product_name>')
def getProduct(product_name):
    productsFound = [
        product for product in products if product['RE']['rutSol'] == product_name.lower()]
    if (len(productsFound) > 0):
        return jsonify({'product': productsFound[0]})
    return jsonify({'error': 'Pedido no encontrado por rut de colaborador'})

#busqueda por numero de pedido.
@app.route('/pedidos_nroPed/<string:product_nroPed>')
def getProductNroPed(product_nroPed):
    productsNroPed = [
        product for product in products if product['RF']['nroPed'] == product_nroPed.lower()]
    if (len(productsNroPed) > 0):
        return jsonify({'product': productsNroPed[0]})
    return jsonify({'error': 'Numero de Pedido no encontrado'})
            
    



if __name__ == '__main__':
    app.run(debug=True, port=4000)