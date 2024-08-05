from flask import Flask , request ,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import os
import hashlib
from flask_jwt_extended import create_access_token , JWTManager
import datetime 
load_dotenv()
app = Flask(__name__)


url = os.getenv("MONGO_URL")
client = MongoClient(url)
db = client["users_db"]
users = db["users"]
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/signup', methods=['POST'])
def register():
    user_data = request.get_json()
    user_data['password'] = hashlib.sha256(user_data["password"].encode("utf-8")).hexdigest()
    usr = users.find_one({"email": user_data["email"]})
    if not usr:
        users.insert_one(user_data)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'User already exists'}), 409
    

@app.route('/login', methods=['POST'])
def login():
    login_details = request.get_json()
    user_from_db = users.find_one({"email": login_details["email"]})
    if user_from_db:
        password = hashlib.sha256(login_details["password"].encode("utf-8")).hexdigest()
        if password == user_from_db["password"]:
            access_token = create_access_token(identity=user_from_db["email"])
            return jsonify(access_token=access_token)
        else:
            return jsonify({'msg': 'Invalid credentials'}), 401
    
if __name__ == '__main__':
    app.run()