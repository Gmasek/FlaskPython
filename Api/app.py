from flask import Flask , request ,jsonify ,Response
from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import os
import hashlib
from flask_jwt_extended import create_refresh_token,create_access_token , get_jwt_identity ,JWTManager , jwt_required
from datetime import timedelta
from flask_cors import CORS , cross_origin
import asyncio
import yfinance as yf
from helpers.utils import getCurrentPrice,getIndicatorColnames , getIndicators

load_dotenv()
app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origins": "*"}})
url = os.getenv("MONGO_URL")
client = MongoClient(url)
db = client["users_db"]
users = db["users"]
jwt = JWTManager(app)
assets = db["assets"]


app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 




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
        
@app.route("/refresh",methods=["POST","OPTIONS"])
@jwt_required()
def refresh():
    if request.method.lower() == 'options':
        return Response()
    current_user = get_jwt_identity() 
    user_db = users.find_one({"email": current_user})
    refresh_token = create_refresh_token(identity=user_db["email"])
    return jsonify(refresh_token=refresh_token),200
    
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
    
@app.route("/getcurrprice",methods=["Post","OPTIONS"])
@jwt_required()
async def  get_curr_price():
    if request.method.lower() == 'options':
        return Response()
    ticker = request.get_json()['ticker']
    try:
        res =  getCurrentPrice(ticker)
        return jsonify(res),200
    except:
        return jsonify({'msg': 'err'}), 404
    
    
@app.route('/getlabels',methods=['GET',"OPTIONS"])
@jwt_required()
def get_all_indicator():
    if request.method.lower() == 'options':
        return Response()
    try:
        res =  getIndicatorColnames()
        return jsonify(res),200
    except:
        return jsonify({'msg': 'err'}), 404

@app.route('/addasset',methods=['POST',"OPTIONS"])
@jwt_required()
def add_asset():
    if request.method.lower() == 'options':
        return Response()
    asset = request.get_json()
    current_user = get_jwt_identity()
    user_email = users.find_one({"email": current_user})['email']
    asset_db = assets.find_one({"ticker": asset['ticker'],"user": user_email, 'qty':asset['qty']})
    if  not asset_db:
        assets.insert_one({"ticker": asset['ticker'],"user": user_email, 'qty':asset['qty'] })
        return jsonify({'msg': 'Asset added successfully'}), 201
    else:
        return jsonify({'msg': 'Error'}), 409   

@app.route("/getassets",methods=["GET","OPTIONS"])
@jwt_required()
def get_assets():
    if request.method.lower() == 'options':
        return Response()
    current_user = get_jwt_identity()
    user_email = users.find_one({"email": current_user})['email']
    assets_db = assets.find({"user": user_email})
    res = []
    for asset in assets_db:
        res.append(
            {"ticker":asset["ticker"],
             "qty":asset["qty"],
             "value":getCurrentPrice(asset["ticker"])})
    if assets_db:
        return jsonify({"message":"success","data":res}), 200
    else:
        return jsonify({'msg': 'User not found'}), 404
        

@app.route("/removeasset",methods=["POST","OPTIONS"])
@jwt_required
def remove_asset():
    if request.method.lower() == 'options': 
        return Response()
    owner = get_jwt_identity()
    email = users.find_one({"email": owner})['email']
    ticker = request.get_json()['ticker']
    asset_db = assets.find_one({"ticker": ticker,"user": email})
    if asset_db:
        assets.delete_one({"ticker": ticker,"user": email})
        return jsonify({'msg': 'Asset removed successfully'}), 200
    else:
        return jsonify({'msg': 'Asset not found'}), 404
        
@app.route("/getindvals",methods=["POST","OPTIONS"])
@jwt_required
def get_ind_vals():
    if request.method.lower() == 'options':
        return Response()   
    ticker = request.get_json()['ticker']
    daysback = request.get_json()['daysback']
    columns = request.get_json()['columns']
    res = getIndicators(ticker,daysback,columns)
    if res:
        return jsonify({"message":"success","data":res}), 200
    else:
        return jsonify({'msg': 'Error getting data'}), 404
        
        
if __name__ == '__main__':
    app.run(debug=True)