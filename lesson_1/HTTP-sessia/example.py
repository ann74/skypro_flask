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


if __name__ == '__main__':
    app.run(debug=True)