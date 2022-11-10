from flask import Flask, redirect, url_for, render_template, request, session, g
from models import db, User, ToDO
from flask_cors import CORS, cross_origin




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
    # session["user_id"]= 2
    # print(session)
    # session.permanent = True
    # # app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    # session.modified = True
    # g.user = User.query.filter_by(username=session.get("user_id")).first() 



@app.route("/")
@cross_origin()
def index():
    # db.create_all()
    response_body = {
        "name": "Rahmin",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body





@app.route("/sign-up", methods=["POST"])
def sign_up():
    user_to_create = User('admin', 'admin@example.com') # make it to where data comes from frontend
    db.session.add(user_to_create)
    db.session.commit()
    pass



@app.route("/sign-in", methods=["POST"])
def sign_in():
    # session["user_id"]= User.query.filter_by(username='username').first()
    # signed_in_user.id
    # signed_in_user.username
    print ("This is request", request.is_json)
    content = request.json
    print("THIS IS CONTENT",content)
    signed_in_user=User.query.filter_by(username=content["username"] , password=content["password"]).first()
    print(type(signed_in_user))
    return {"username": signed_in_user.username, "password": signed_in_user.password}



@app.route("/create-a-to-do", methods=["POST"])
def create_to_do():
    to_do_create = ToDO("title", "description", "due_date")
    pass


@app.route("/edit-to-do", methods=["POST"])
def edit_to_do():
    pass



@app.route("/delete-to-do", methods=["POST"])
def delete_to_do():
    pass






if __name__ == "__main__":
    app.run(port=5000)
