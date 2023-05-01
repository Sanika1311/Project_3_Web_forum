from flask import Flask, request, jsonify
import secrets
from datetime import datetime
import threading

app = Flask(__name__)

users = []
posts = []
postId = 0
userId = 0

threadLock = threading.Lock()

@app.route("/")
def hello_world():
    print("hello")
    return "<h1>Hello, World!</h1>"

@app.route("/users/<int:user_id>/post", methods=['POST'])
def post_method(user_id):
    try :
        with threadLock:
            # print(request.get_json())
            data = request.get_json()
            if(data == None):
                return {'err': 'bad request'},400
            
            elif ('msg' not in data or  not isinstance(data['msg'],str)):
                return {'err': 'bad request'},400
            
            elif(not isinstance(data['msg'],str)):
                return {'err': 'bad request'},400
            
            elif (user_id <= 0):
                return {'err': 'bad request'},400
            
            else:  
                msg = data['msg']
                global postId
                id = postId + 1
                postId = postId +1
                key = secrets.token_hex(15)
                timestamp = datetime.now().utcnow().isoformat()
                user = find_users(user_id)
                if user == None:
                    return {'err': 'not found - User not found of the given ID'},404

                posts_data = {'id': id, 'user key': user['key'],'key' : key, 'msg' : msg, 'timestamp': timestamp, 'user ID' : user_id}
                posts.append(posts_data)
                print(posts)
                return jsonify(posts_data), 200
    except Exception as e:
        return {'err': 'bad request'},400



# @app.route("/post", methods=['POST'])
# def post_method():
#     try :
#         with threadLock:
#             data = request.get_json()
#             if(data == None):
#                 return {'err': 'bad request'},400
            
#             elif ('msg' not in data or  not isinstance(data['msg'],str)):
#                 return {'err': 'bad request'},400
            
#             elif(not isinstance(data['msg'],str)):
#                 return {'err': 'bad request'},400
            
#             # elif (user_id <= 0):
#             #     return {'err': 'bad request'},400
            
#             else:  
#                 msg = data['msg']
#                 global postId
#                 id = postId + 1
#                 postId = postId +1
#                 key = secrets.token_hex(15)
#                 timestamp = datetime.now().utcnow().isoformat()
#                 # user = find_users(user_id)
#                 # if user == None:
#                 #     return {'err': 'not found - User not found of the given ID'},404

#                 posts_data = {'id': id, 'key' : key, 'msg' : msg, 'timestamp': timestamp}
#                 posts.append(posts_data)
#                 # print(posts)
#                 return jsonify(posts_data), 200
#     except Exception as e:
#         return {'err': 'bad request'},400

@app.route("/users/<int:user_id>/post/<int:post_id>", methods=['GET'])
def get_method(user_id,post_id):
    # print(postid)
    try :
        with threadLock:
            if(post_id <= 0 and user_id):
                return {'err': 'bad request'},400
            
            elif not isinstance(post_id, int):
                return {'err': 'bad request'},400

            else:
                post = find_posts(post_id)
                if post == None:
                    return {'err': 'not found'},404 
                
               #post key needs to validated
                elif post['user ID'] != user_id:
                    return {'err': 'bad request'},400
                
                else:
                    if(isinstance(post['id'], int) and isinstance(post['msg'],str)): #check for the date is remaining
                        # return {'id': post['id'],'msg': post['msg'], 'timestamp' : post['timestamp']}, 200
                        return {'id': post['id'],'msg': post['msg'], 'timestamp' : post['timestamp'], 'user ID' : post['user ID']}, 200
                    
    except Exception as e:
        return {'err': 'bad request'},400

           
@app.route("/post/<int:id>/delete/<string:key>", methods=['DELETE'])
def delete_method(id,key):
    #ater deleting the post it is also a new post so it will return a new key for put it updates the whole post.check for the keys
    #remaining : timestamp
    try :
        with threadLock:
            if(id <= 0):
                return {'err': 'bad request'},400
            else:
                post = find_posts(id)
                # print(post)
                if post == None:
                    return {'err': 'not found'},404
                elif(post['key'] != key):
                    return {'err': 'forbidden'},403
                else:
                    # updated_post = {'id' : id,'msg' : post['msg'],  'key' :secrets.token_hex(15),'timestamp' : datetime.now().utcnow().isoformat()}
                    updated_post = {'id' : id,'msg' : post['msg'], 'user ID' : post['user ID'], 'key' :secrets.token_hex(15),'timestamp' : datetime.now().utcnow().isoformat()}
                    posts.remove(post)
                    return updated_post,200
    except Exception as e:
        return {'err': 'bad request'},400

# #extension 2 : 
@app.route("/users", methods=["POST"])
def signup():
    #make username and id unique add the code for that - username is unique done
    try :
        with threadLock:
            data = request.get_json()
            if(data == None):
                return {'err': 'bad request'},400
            
            elif ('username' not in data or  not isinstance(data['username'],str)):
                return {'err': 'bad request'},400
            
            elif ('email address' not in data or  not isinstance(data['email address'],str)):
                return {'err': 'bad request'},400
            
            

            else:
                username = data['username']
                email = data['email address']

                if('moderator' not in data):
                    moderator = False
                    moderator_key = None
                else:
                    moderator = True
                    moderator_key = secrets.token_hex(15)
                
                found_user_dicts = [user_dict for user_dict in users if user_dict.get('username') == username]
                if found_user_dicts:
                    return {'err': 'bad request - Username should be unique'},400
                else: 
                    global userId
                    userId = userId + 1
                    key =  secrets.token_hex(15)
                    timestamp = datetime.now().utcnow().isoformat()
                    user_data = {'username' : username, 'id' : userId, 'email address' : email, 'key' : key, 'timestamp': timestamp, 'moderator' : moderator, 'moderator key' : moderator_key}
                    print(userId)
                    print(username)
                    print(key)
                    users.append(user_data)
                    return user_data,200
    except Exception as e:
        return {'err': e},400


@app.route("/users/<int:id>", methods=["GET"])
def get_users(id):
    try :
        with threadLock:
            if(id <= 0):
                return {'err': 'bad request'},400
            else:
                user = find_users(id)
                if user == None:
                    return {'err': 'not found'},404 
                else:
                    if(isinstance(user['id'], int)): #check for the date is remaining
                        return {'id': user['id'],'username' : user['username'], 'email' : user['email address'], 'timestamp': user['timestamp'], 'posts' : user['posts']}, 200
    except Exception as e:
        return {'err': 'bad request '},400
    
@app.route("/users/<string:username>", methods=["GET"])
def get_users_username(username):
    try :
        with threadLock:
            if not isinstance(username, str):
                return {'err': 'bad request'},400
            else:
                user = next((item for item in users if item['username'] == username), None)
                if user == None:
                    return {'err': 'not found'},404 
                else:
                    if(isinstance(user['id'], int)): #check for the date is remaining
                        return {'id': user['id'],'username' : user['username'], 'email' : user['email address'], 'timestamp': user['timestamp'], 'posts' : user['posts']}, 200
    except Exception as e:
        return {'err': 'bad request'},400



@app.route("/users/edit/<string:key>",methods=["PUT"])
def edit_user(key):
    try :
        with threadLock:
            data = request.get_json()

            if(data == None):
                return {'err': 'bad request'},400
            
            elif 'username' in data and 'email address' in data:
                username = data['username']
                email = data['email address']
                if(find_user_username(username)):
                    return {'err': 'bad request - Username should be unique'},400
                user = find_users_keys(key)
                if user == None:
                    return {'err': 'not found'},404
                elif(user['key'] != key):
                    return {'err': 'forbidden'},403
                else:
                    user['username'] = username
                    user['email address'] = email
                    user['timestamp'] = datetime.now().utcnow().isoformat()
                    return user,200
                
            elif 'username' in data :
                if not isinstance(data['username'],str):
                    return {'err': 'bad request'},400
                else :
                    username = data['username']

                    if(find_user_username(username)):
                        return {'err': 'bad request - Username should be unique'},400
                    
                    user = find_users_keys(key)
                    if user == None:
                        return {'err': 'not found'},404
                    elif(user['key'] != key):
                        return {'err': 'forbidden'},403
                    else:
                        user['username'] = username
                        user['timestamp'] = datetime.now().utcnow().isoformat()
                        return user,200
                    
            elif 'email address' in data :
                if not isinstance(data['email address'],str):
                    return {'err': 'bad request'},400
                else :
                    email = data['email address']
                    user = find_users_keys(key)
                    if user == None:
                        return {'err': 'not found'},404
                    elif(user['key'] != key):
                        return {'err': 'forbidden'},403
                    else:
                        user['email address'] = email
                        user['timestamp'] = datetime.now().utcnow().isoformat()
                        return user,200
                    
            else:
                return {'err': 'bad request'},400
    except Exception as e:
        return {'err': 'bad request'},400
    
#let user search for posts based by a given user.
#extension 3
@app.route("/users/search/<int:id>",methods = ["GET"])
def search_posts(id):
    try :
        with threadLock:
            if(id <= 0):
                return {'err': 'bad request'},400
            else:
                user_post = [post for post in posts if post.get('user ID') == id]
                print(user_post)
                if user_post == None:
                    return {'err': 'not found'},404 
                else:
                    return user_post,200
                  
    except Exception as e:
        return {'err': 'bad request'},400
    
#extension 4 - delete
@app.route("/users/<string:moderator_key>/delete/<int:id>", methods=['DELETE'])
def delete_user(moderator_key,id):
    try :
        with threadLock:
            if(id <= 0):
                return {'err': 'bad request'},400
            else:
                user = find_users_keys(moderator_key)
                # print(post)
                if user == None:
                    return {'err': 'not found-User is not a moderator'},404
                elif(user['key'] != moderator_key):
                    return {'err': 'forbidden'},403
                else:
                    # updated_post = {'id' : id,'msg' : post['msg'],  'key' :secrets.token_hex(15),'timestamp' : datetime.now().utcnow().isoformat()}
                    post = find_posts(id)
                    if post == None:
                        return {'err': 'not found- Post not found'},404
                    else:
                        posts.remove(post)
                        return {'msg' : 'Post deleted successfully'},200
        
    except Exception as e:
        return {'err': 'bad request'},400


@app.route('/posts/search', methods=['GET'])
def search_posts_time():
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    
    if not start_time_str and not end_time_str:
        return jsonify(error='bad request - At least one of start_time or end_time must be provided.'), 400
    print(start_time_str)
    print(end_time_str)
    if start_time_str:
        try:
                
                start_date = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
                print(start_date)
    
        except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO 8601 format.'}), 400
    else:
        start_date = None

    if end_time_str:
        try:
            end_date = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')
            
            print(end_date)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use ISO 8601 format.'}), 400
    else:
        end_date = None
    
    print(start_date)
    print(end_date)
    # try:
    #     if start_time_str:
    #         start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=datetime.timezone.utc)
    #     else:
    #         start_time = datetime.min.replace(tzinfo=datetime.timezone.utc)
            
    #     if end_time_str:
    #         end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=datetime.timezone.utc)
    #     else:
    #         end_time = datetime.max.replace(tzinfo=datetime.timezone.utc)
    # except ValueError:
    #     return jsonify(error='Invalid start_time or end_time format. Must be ISO 8601 timestamp in UTC.'), 400
    
    matched_posts = []
    
    for post in posts:
        # post_time = datetime.fromisoformat(post['timestamp']).replace(tzinfo=datetime.timezone.utc)
        post_date = datetime.strptime(post['timestamp'], '%Y-%m-%dT%H:%M:%S')
        if start_date <= post_date <= end_date:
            matched_posts.append(post)
    
    return jsonify(posts=matched_posts)



def find_posts(id):
    my_item = next((item for item in posts if item['id'] == id), None)
    return my_item

def find_users(id):
    my_item = next((item for item in users if item['id'] == id), None)
    return my_item

def find_users_keys(key):
    my_item = next((item for item in users if item['key'] == key), None)
    return my_item

def find_user_username(username):
    my_item = next((item for item in users if item['username'] == username), None)
    return my_item



if __name__ == '__main__':
    app.run(debug=True)


#{
#     "username": "Sanika",
#     "email address": "12334433"
# }