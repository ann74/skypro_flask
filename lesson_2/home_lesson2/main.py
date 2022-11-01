from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/users/<id>')
def get_user(id):
    return render_template('users/show.html', id=id)


@app.route('/users/')
def users():
    users = ['mike', 'mishel', 'adel', 'keks', 'kamila']
    term = request.args.get('term')
    if not term:
        term = ''
    filtred_users = filter(lambda x: term in x, users)
    return render_template('users/index.html', users=filtred_users, search=term)


if __name__ == '__main__':
    app.run(debug=True)
