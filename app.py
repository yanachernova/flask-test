import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo
'''for find the place of the file that we are executing '''
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
app = Flask(__name__)
''' for the case that i forget de slash on the endpoint '''
app.url_map.strict_slashes = False 
''' for the show or not the errors '''
app.config['DEBUG'] = True
''' for configuration of the environment '''
app.config['ENV'] = 'development'
'''for define my database route and configuration'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
'''is required when i use SQLALCHEMY and for delete not important changes '''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
''' for configuration of command to migrate '''
db.init_app(app)
migrate = Migrate(app, db)
''' for start de liveServer '''
manager = Manager(app)
''' run for console the migrate command '''
manager.add_command('db',MigrateCommand)
''' for use the development environment '''
CORS(app)
''' for define the route for default '''
@app.route('/')
def home():
    return render_template('index.htm', name='home')
''' for consulting my API '''

@app.route('/api/<user>/todos', methods=['GET','POST'])
@app.route('/api/<user>/todos/<int:id>', methods=['GET','PUT','DELETE'])
def todos(user, id=None):
    if request.method=='GET':
        if id is not None:
            todo = Todo.query.filter_by(user=user).get(id)
            if todo:
                return jsonify(todo.serialize()),200
            else:
                return jsonify({'msg':'Not Found'}),404
        else:            
            todos = Todo.query.filter_by(user=user).all() #toma todos los contactos
            todos = list(map(lambda todo: todo.serialize(), todos)) #me devuelve un diccionario (arreglo) de elementos dentro de contactos, generando un nuevo arreglo de contactos
            return jsonify(todos), 200
    if request.method == 'POST':
        if not request.json.get('label'):
            return jsonify({'label':'is required'}),422 #error code return
        #if not request.json.get('done'):
        #    return jsonify({'done':'is required'}),422 #error code return
        '''For insert a new contact in our database'''
        todo = Todo() # This line is onnected to other sheet
        todo.label = request.json.get('label')
        todo.done = request.json.get('done') 
        todo.user = user
        db.session.add(todo)  
        db.session.commit()
        '''For return 201 code if is a correct new contact '''    
        return jsonify(todo.serialize()),201    
    if request.method == 'PUT':
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"todo":"Not Found"}),404
        if not request.json.get('label'):
            return jsonify({'label':'is required'}),422 #error code return
        if not request.json.get('done'):
            return jsonify({'done':'is required'}),422 #error code return
        '''For insert a new contact in our database'''
        todo.label = request.json.get('label')
        todo.done = request.json.get('done')   
        db.session.commit()
        '''For return 201 code if is a correct new contact '''    
        return jsonify(todo.serialize()),201      
    if request.method == 'DELETE':
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"msg":"Not Found"}), 404
        db.session.delete(todo)
        return jsonify({"msg":"Contact Deleted"}), 404


''' for start my app'''
if __name__=='__main__':
    manager.run()