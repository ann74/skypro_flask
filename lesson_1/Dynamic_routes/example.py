from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to Flask!'

@app.get('/users')
def users_get():
    return 'GET /users'

@app.post('/users')
def users():
    return 'Users', 302

@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'

if __name__ == '__main__':
    app.run(debug=True)