from flask import Flask, request
import secrets
from datetime import datetime

app = Flask(__name__)

posts = []

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/post", methods=['POST'])
def post_method():
    
    print(request.get_json())
    data = request.get_json()
    if(data == None):
        return {'err': 'bad request'},400
    
    elif ('msg' not in data or  not isinstance(data['msg'],str)):
        return {'err': 'bad request'},400
    
    elif(not isinstance(data['msg'],str)):
        return {'err': 'bad request'},400
    
    else:  
        msg = data['msg']
        id = len(posts)+1
        key = secrets.token_hex(15)
        timestamp = datetime.now().utcnow().isoformat()

        posts_data = {'id': id, 'key': key, 'msg' : msg, 'timestamp': timestamp}
        posts.append(posts_data)
        print(posts)
        return posts_data, 200

@app.route("/post/<int:id>", methods=['GET'])
def get_method(id):
    if(id <= 0):
        return {'err': 'bad request'},400
    else:
        post = find_posts(id)
        if post == None:
            return {'err': 'not found'},404 
        else:
            if(isinstance(post['id'], int) and isinstance(post['msg'],str)): #check for the date is remaining
                return {'id': post['id'],'msg': post['msg'], 'timestamp' : post['timestamp']}, 200
            
       

@app.route("/post/<int:id>", methods=['DELETE'])
def delete_method(id):
    if(id <= 0):
        return {'err': 'bad request'},400
    else:
        for i in posts:
            if(i['id'] == id):
                posts.remove(i)
                return {'msg': 'ok'}, 200
        return {'err': 'not found'},404

def find_posts(id):
    my_item = next((item for item in posts if item['id'] == id), None)
    return my_item
    
if __name__ == '__main__':
    app.run(debug=True)


