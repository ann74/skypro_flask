from flask import Flask, request, render_template
from random import choice

app = Flask(__name__)


@app.route('/')
def hello():
    user_data = {
        "name": "Ivan",
        "phone": "+7 123 456 78 90",
        "email": "ivan_dev@gmail.com",
        "telegram": "ivan_dev",
    }
    items = ["Python", "Java", "Kotlin", "Go"]
    is_blocked = choice([True, False])
    return render_template('index.html', user=user_data, items=items,
                           is_blocked=is_blocked)


@app.route('/users/<id>')
def users(id):
    return render_template(
        'index1.html',
        name=id,
    )


if __name__ == '__main__':
    app.run(debug=True)
