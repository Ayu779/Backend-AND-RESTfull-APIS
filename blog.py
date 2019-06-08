from flask import Flask, request,jsonify
from pymongo import MongoClient
from random import randint
from datetime import datetime
app = Flask(__name__)
client = MongoClient()
db = client.db
tweets = db.tweets
__id=1000
@app.route('/twitter', methods=['GET','POST','PUT','DELETE'])
def twitter():
	if request.method =='POST':
		data = request.json
		name = data.get('name', 'Amitabh Bacchan')
		message = data.get('message', 'Hii')
		Likes = 0
		global __id
		x = str(__id)
		res = tweets.insert_one({
		'name' : name,
		'Tweet' : message,
		'Likes' : Likes,
		'active' : True,
		'id' : x
		})
		__id=int(__id) - 1 
		response = {
		'alert' : 'Tweeted Successfuylly'
		}
		return jsonify(response), 201


	elif request.method == 'GET':
		#__id= request.args.get('id')
		res = tweets.find({},{'_id':0})
		response = {
			'data' : list(res)
        }
		return jsonify(response)
		
		
	elif request.method == 'PUT':
		tweetid=request.json.get('id',0)
		result=tweets.update({"id":tweetid},{"$inc":{"Likes":1}})
		response={
           	'alert':'Like  + +'
		}

		return jsonify(response)
	else:
		tweetid=request.json.get('id',0)
		result=tweets.update({"id":tweetid},{"$set":{"active": "False"}})
		response = {
		'message' : 'Deleted tweet'
		}

		return jsonify(response)


if __name__ == '__main__':
	app.run(debug=True, use_reloader=True, port=80)
