from flask import Flask , request ,jsonify ,Response
from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import os
import hashlib
from flask_jwt_extended import create_refresh_token,create_access_token , get_jwt_identity ,JWTManager , jwt_required
import datetime 
from flask_cors import CORS , cross_origin
load_dotenv()
app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origins": "*"}})
url = os.getenv("MONGO_URL")
client = MongoClient(url)
db = client["users_db"]
users = db["users"]
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) 

@app.route('/')
def hello_world():
    return 'Hello World!'



@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/signup', methods=['POST',"OPTIONS"])
def register():
    if request.method.lower() == 'options':
        return Response()
    user_data = request.get_json()
    user_data['password'] = hashlib.sha256(user_data["password"].encode("utf-8")).hexdigest()
    usr = users.find_one({"email": user_data["email"]})
    if not usr:
        users.insert_one(user_data)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'User already exists'}), 409
    

@app.route('/login', methods=['POST',"OPTIONS"])
def login():
    if request.method.lower() == 'options':
        return Response()
    login_details = request.get_json()
    user_from_db = users.find_one({"email": login_details["email"]})
    if user_from_db:
        password = hashlib.sha256(login_details["password"].encode("utf-8")).hexdigest()
        if password == user_from_db["password"]:
            access_token = create_access_token(identity=user_from_db["email"])
            refresh_token = create_refresh_token(identity=user_from_db["email"])
            return jsonify(access_token=access_token,refresh_token=refresh_token)
        else:
            return jsonify({'msg': 'Invalid credentials'}), 401
    
@app.route('/getuser',methods=['GET',"OPTIONS"])
@jwt_required()
def get_user():
    if request.method.lower() == 'options':
        return Response()
    current_user = get_jwt_identity()
    try:
        
        user_db = users.find_one({"email": current_user})
        print(user_db["email"])
    except:
        return jsonify({'msg': 'User not found'}), 404
    
    if user_db:
        return jsonify({"message":"success","data":user_db["email"]}), 200
    else:
        return jsonify({'msg': 'User not found'}), 404
    


if __name__ == '__main__':
    app.run()