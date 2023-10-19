from flask import Flask, request, jsonify
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
CORS(app)

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

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

# Schémas de sérialisation
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'tasks')

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'user_id')

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
        return jsonify(access_token=access_token)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# ...

# Routes of Task
# ...



@app.route('/task', methods=['POST'])
@jwt_required()
def add_task():
    # token = request.headers.get('Authorization').split(" ")[1]  # Récupère le token JWT de l'en-tête
    # current_user_id = get_user_id_from_token(token)  # Récupère l'ID de l'utilisateur à partir du token

    # if current_user_id is None:
    #     return jsonify({'message': 'Erreur lors de la récupération de l\'ID de l\'utilisateur.'}), 401
    user_id = request.json['id']
    name = request.json['name']
    content = request.json['content']
    tag = request.json.get('tag', 'init')  # 'init' sera la valeur par défaut si 'tag' n'est pas fourni
    due_date = datetime.strptime(request.json['due_date'], '%Y-%m-%d %H:%M:%S')

    new_task = Task(name=name, content=content, tag=tag, due_date=due_date, user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


@app.route('/task', methods=['GET'])
def get_all_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/task/me', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    return task_schema.jsonify(task)

@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    name = request.json['name']
    content = request.json['content']
    tag = request.json.get('tag', task.tag)  # Conserve la valeur actuelle si 'tag' n'est pas fourni
    due_date = datetime.strptime(request.json['due_date'], '%Y-%m-%d %H:%M:%S')

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
