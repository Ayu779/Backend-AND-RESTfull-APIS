from flask import Flask, request,jsonify,json
from pymongo import MongoClient
from passlib.hash import sha256_crypt
import jwt
from werkzeug.security import generate_password_hash, safe_str_cmp
app=Flask(__name__)
client = MongoClient()
db = client.db
users=db.user
secretkey = "reportpro"
@app.route('/user',methods=['POST','GET'])
def ayush():
    if request.method =='POST':
        data = request.json
        user_id = data.get('userid')
        phoneno = data.get('phoneno')
        name = data.get('name')
        pas = sha256_crypt.encrypt(data.get('pas'))
        if user_id:
            extra = users.find_one({"Userid" : user_id},{'_id':0})
            if extra:
                response = {
                    'alert' : 'Username Already Taken'
                }
            else:
                res = users.insert_one({
                    'Name': name,
                    'Userid': user_id,
                    'Phone No': phoneno,
                    'Password': pas
                })
                response = {
                    'alert': 'Registered Successfully'
                }
        else:
            response= {
                'alert' : "Userid cannot be null"
            }
        return jsonify(response), 201

    elif request.method == 'GET':
        result = users.find({}, {'_id': 0})
        response = {
            'data': list(result)
        }
        return jsonify(response)

@app.route('/user/<user_id>', methods = ['GET'])
def find_one(user_id):
    if request.method == 'GET':
        user = user_id
        result = users.find({"Userid" : user},{'_id':0})
        response = {
            'data': list(result)
        }
        return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    userid= request.json.get('userid')
    pas =  request.json.get('pas')
    secured = sha256_crypt.encrypt(pas)
    result = users.find_one({"Userid" : userid})


    if result:
        if sha256_crypt.verify(pas, result['Password']):
            access_token = jwt.encode({
                'Name' : result['Name'],
                'Userid' : result['Userid'],
                'Phone No' : result['Phone No']},secretkey
            )
            aa=access_token.decode('ascii')
            response = {
                "token" : aa
            }
            return jsonify(response)
        else:
            response = {
                "error": "Invalid Username and Password"
            }
            return jsonify(response)
    else:
       response = {
           "result": "No result found"
       }
       return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
