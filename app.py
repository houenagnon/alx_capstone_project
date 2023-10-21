from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, decode_token
from flask_cors import CORS

# Initialisation de l'application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://todoUser:todo123@localhost/ToDo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'AZSKL?NB515hjb'  # Remplacez par votre clé secrète réelle
jwt = JWTManager(app)

# Initialisation de la base de données
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Modèles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password =password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    content= db.Column(db.String(500), nullable=False)
    tag = db.Column(db.String(50), default='init')
    due_date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                
    def __init__(self,name, content, tag, due_date, user_id):
        self.name = name
        self.content = content
        self.tag = tag
        self.due_date = due_date
        self.user_id = user_id

# Schémas de sérialisation
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'tasks')

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'content', 'tag', 'due_date', 'date_created', 'user_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Routes
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_user = User(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@app.route('/login', methods=['POST'])
def login_user():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, username=user.username, how=user.id)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# ...

# Routes of Task
# ...


@app.route('/task', methods=['POST'])
def add_task():
    user_id = request.json['id']
    name = request.json['name']  # Ajoutez cette ligne pour récupérer le champ 'name'
    content = request.json['content']
    tag = request.json.get('tag', 'init')
    due_date = request.json['due_date']

    new_task = Task(name=name, content=content, tag=tag, due_date=due_date, user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


    

@app.route('/task/<user_id>', methods=['GET'])
def get_all_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    result = tasks_schema.dump(tasks)

    return jsonify(result)

@app.route('/task/by/<task_id>', methods=['GET'])
def get_tasks(task_id):
    tasks = Task.query.filter_by(id=task_id).all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)




@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    name = request.json['name']
    content = request.json['content']
    tag = request.json.get('tag', task.tag)  # Conserve la valeur actuelle si 'tag' n'est pas fourni
    due_date = request.json['due_date']

    task.name = name
    task.content = content
    task.tag = tag
    task.due_date = due_date    

    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# ...



with app.app_context():
    db.create_all()
if __name__ == '__main__':
    # 
    app.run(debug=True)
