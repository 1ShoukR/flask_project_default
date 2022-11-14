from flask import Flask, redirect, url_for, render_template, request, session, g
from models import db, User, ToDO
from flask_cors import CORS, cross_origin
import json
import os
from datetime import datetime



# Flask
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Rahmin12@localhost:3306/to_do_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)


@app.before_request
def before_request():
    print("before request")
    print("this is session", session)
    g.user = None
    if os.path.isfile("session.json"):
        print ("File exists and is readable")
        with open('session.json', 'r') as f:
            data = json.load(f)
            g.user = User.query.filter_by(id=data["id"]).first()    

    # session["user_id"]= 2
    # if "user_id" in session.keys():
        

    # print(session)
    # session.permanent = True
    # # app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    # session.modified = True
    # g.user = User.query.filter_by(username=session.get("user_id")).first() 



@app.route("/")
@cross_origin()
def index():
    db.create_all()
    response_body = {
        "name": "Rahmin",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body





@app.route("/sign-up", methods=["POST"])
def sign_up():
    incoming_data = request.json
    print("This is incoming_data", incoming_data)
    user_to_create = User(username=incoming_data["username"] , password=incoming_data["password"]) 
    db.session.add(user_to_create)
    db.session.commit()
    return {"username": user_to_create.username, "password": user_to_create.password}



@app.route("/sign-in", methods=["POST"])
@cross_origin()
def sign_in():
    # session["user_id"]= User.query.filter_by(username='username').first()
    # signed_in_user.id
    # signed_in_user.username
    print ("This is request", request.is_json)
    content = request.json
    print("THIS IS CONTENT",content)
    signed_in_user=User.query.filter_by(username=content["username"] , password=content["password"]).first()
    get_table_data=ToDO.query.filter_by(user_id=signed_in_user.id).all()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed
        })
    print(response_table_data)
    print(type(signed_in_user))
    response = {
        "username": signed_in_user.username,
        "password": signed_in_user.password,
        "id": signed_in_user.id,
    }
    with open("session.json", "w") as outfile:
        outfile.write(json.dumps(response, indent=4))
    return {"username": signed_in_user.username, "password": signed_in_user.password, "toDos": response_table_data,}


@app.route("/get-to-do", methods=["GET"])
@cross_origin()
def get_to_do():
    
    pass


@app.route("/create-a-to-do", methods=["POST"])
@cross_origin()
def create_to_do():
    print("This is request", request.json)
    content = request.json
    print("THIS IS CONTENT", content)
    order_query_data = ToDO.query.filter_by(user_id=g.user.id).order_by(ToDO.order_of_to_do).all()
    if len(order_query_data) == 0:
        to_do_create = ToDO(user_id=g.user.id, title=content["title"], description=content["description"], due_date=content["date"], order_of_to_do=1)
    else:
        to_do_create = ToDO(user_id=g.user.id, title=content["title"], description=content["description"], due_date=content["date"], order_of_to_do=order_query_data[-1].order_of_to_do+1)
    db.session.add(to_do_create)
    db.session.commit()
    get_table_data=ToDO.query.filter_by(user_id=g.user.id).all()
    print("This is queried table",get_table_data)
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed,
            "order_of_to_do": table_data.order_of_to_do
        })
    print(response_table_data)
    return response_table_data


@app.route("/edit-to-do", methods=["POST"])
def edit_to_do():
    content = request.json
    print("this is content", content)
    to_do_edit = ToDO.query.filter_by(id=content["id"]).first()
    to_do_edit.title = content["title"]
    to_do_edit.description = content["description"]
    to_do_edit.due_date = content["due_date"]
    to_do_edit.completed = content["completed"]
    db.session.commit()
    get_table_data=ToDO.query.filter_by(user_id=g.user.id).all()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed
    })
    return response_table_data



@app.route("/delete-to-do", methods=["POST"])
def delete_to_do():
    content = request.json
    print("this is content", content)
    to_do_delete = ToDO.query.filter_by(id=content["id"]).first()
    db.session.delete(to_do_delete)
    db.session.commit()
    ordered_todo= ToDO.query.filter_by(user_id=g.user.id).order_by(ToDO.order_of_to_do).all()
    count = 0
    for todo in ordered_todo:
        todo.order_of_to_do = count
        count += 1
    db.session.commit()
    get_table_data=ToDO.query.filter_by(user_id=g.user.id).all()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed
        })
    return response_table_data


@app.route("/mark-as-complete", methods=["POST"])
def mark_as_complete():
    content = request.json
    print("this is content", content)
    mark_as_complete = ToDO.query.filter_by(id=content["id"]).first()
    mark_as_complete.completed = True
    get_table_data = ToDO.query.filter_by(user_id=g.user.id).all()
    db.session.commit()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed
        })
    print(response_table_data)
    return response_table_data


@app.route("/re-order-up", methods=["POST"])
def re_order_up():
    content = request.json
    print("this is content", content)
    to_do_re_order= ToDO.query.filter_by(id=content["id"]).first()
    to_do_re_order.order_of_to_do -= 1
    db.session.commit()
    entry_before_it= ToDO.query.filter_by(user_id=g.user.id).order_by(ToDO.order_of_to_do).all()
    for entry in entry_before_it:
        count = entry.order_of_to_do
        count -=1
    db.session.commit()
    get_table_data=ToDO.query.filter_by(user_id=g.user.id).all()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed,
            "order_of_to_do": table_data.order_of_to_do
        })
    return response_table_data


@app.route("/re-order-down", methods=["POST"])
def re_order_down():
    content = request.json
    print("this is content", content)
    to_do_re_order = ToDO.query.filter_by(id=content["id"]).first()
    to_do_re_order.order_of_to_do += 1
    db.session.commit()
    entry_before_it= ToDO.query.filter_by(user_id=g.user.id).order_by(ToDO.order_of_to_do).all()
    for entry in entry_before_it:
        count = entry.order_of_to_do
        count += 1
    db.session.commit()
    get_table_data=ToDO.query.filter_by(user_id=g.user.id).all()
    response_table_data = []
    for table_data in get_table_data:
        print(table_data)
        response_table_data.append({
            "id": table_data.id,
            "title": table_data.title,
            "description": table_data.description,
            "due_date": table_data.due_date,
            "completed": table_data.completed,
            "order_of_to_do": table_data.order_of_to_do
        })
    return response_table_data 


if __name__ == "__main__":
    app.run(port=5000)
