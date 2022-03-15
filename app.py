#from flask import Flask, render_template, jsonify, request
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
#cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "bigbuda2022"
jwt = JWTManager(app)


#cors validate dominios o ip
CORS(app,resource={r"/pedidos/*":{"origins":"http://localhost"}})
from pedidos import products


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



#busqueda@cross_origin
@app.route("/")
def index():
  return render_template('index.html')
    
#ver todos los pedidos exportados
@app.route('/pedidos')
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