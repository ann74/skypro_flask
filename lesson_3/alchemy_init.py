from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import prettytable
from sqlalchemy import or_, desc, func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age > 17'))
    group_id = db.Column(db.Integer, db.ForeignKey("group1.id"))
    groups = relationship("Group")


class Group(db.Model):
    __tablename__ = "group1"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = relationship("User", overlaps="groups")

with app.app_context():
    db.drop_all()
    db.create_all()

group_01 = Group(id=1, name='Group1')
user_01 = User(id=1, passport_number='062 342156', name='John', age=23, groups=group_01)

user_02 = User(id=2, passport_number='062 342157', name='Katy', age=25)
group_02 = Group(id=2, name='Group2', users=[user_02])

user_03 = User(id=3, passport_number='062 342158', name='Artur', age=20, groups=group_01)
user_04 = User(id=4, passport_number='065 342158', name='Maxim', age=26, groups=group_01)
user_05 = User(id=5, passport_number='063 342160', name='Lily', age=19, groups=group_02)
user_06 = User(id=6, passport_number='064 342170', name='Mary', age=25)

with app.app_context():
    db.session.add(user_01)
    db.session.add(group_02)
    db.session.add_all([user_03, user_04, user_05, user_06])
    db.session.commit()
    # Вывод одной таблицы в красивом виде
    cursor = db.session.execute("SELECT * from users").cursor
    print(prettytable.from_db_cursor(cursor))
    # Доступ к полям таблицы group1 через юзера
    user_with_group = User.query.get(1)
    print(user_with_group.groups.name)
    # запросы на выборку
    query1 = User.query.filter(User.age >20, User.id < 5)  # условие and
    print(f'Запрос: {query1}\nРезультат: {query1.all()}')
    query2 = User.query.filter(or_(User.age > 20, User.id < 5))  # условие or
    print(f'Запрос: {query2}\nРезультат: {query2.all()}')
    query3 = User.query.filter(User.name.like('M%'))
    print(f'Запрос: {query3}\nРезультат: {query3.all()}')
    query4 = User.query.filter(User.groups == None)  # is Null
    print(f'Запрос: {query4}\nРезультат: {query4.all()}')
    query5 = User.query.filter(User.age.in_([25, 26]))  # in (.,.)
    print(f'Запрос: {query5}\nРезультат: {query5.all()}')
    query6 = User.query.filter(User.age.notin_([25, 26]))  # not in (.,.)
    print(f'Запрос: {query6}\nРезультат: {query6.all()}')
    query7 = User.query.filter(User.age.between(20, 25))  # benween a and b
    print(f'Запрос: {query7}\nРезультат: {query7.all()}')
    query8 = User.query.limit(2).offset(2)  # limit a offset b
    print(f'Запрос: {query8}\nРезультат: {query8.all()}')
    query9 = User.query.order_by(User.age)  # order by
    print(f'Запрос: {query9}\nРезультат: {query9.all()}')
    query10 = User.query.order_by(desc(User.age))  # order by desc
    print(f'Запрос: {query10}\nРезультат: {query10.all()}')
    query11 = db.session.query(User.name, Group.name).join(Group)  # join
    print(f'Запрос: {query11}\nРезультат: {query11.all()}')
    query12 = db.session.query(func.count(User.id)).join(Group).filter(Group.id == 1).group_by(Group.id)  # group by
    print(f'Запрос: {query12}\nРезультат: {query12.scalar()}')
    # Изменение данных в таблице
    user = User.query.get(3)
    print(user.name)
    user.name = 'Artur_new'
    db.session.add(user)
    db.session.commit()
    user = User.query.get(3)
    print(user.name)
    # удаление данных
    User.query.filter(User.age < 20).delete()
    db.session.commit()

# Работа с транзакциями
user_07 = User(passport_number='062 352158', name='Petr', age=18, groups=group_01)
user_08 = User(passport_number='065 342658', name='Sergey', age=45, groups=group_01)
user_09 = User(passport_number='063 372160', name='Lena', age=30, groups=group_02)
user_10 = User(passport_number='064 342180', name='Sveta', age=24)
with app.app_context():
    with db.session.begin(): # внешняя транзакция, закомитится все, если выполнится все внутри сессии
        db.session.add(user_07)
        db.session.add(user_08)
        nested = db.session.begin_nested()  # вложенная транзакция
        try:
            db.session.add(user_09)
            db.session.add(user_10)
            # raise Exception('Database Exeption')
        except Exception as e:
            print(e)
            nested.rollback()






@app.route("/users/first")
def get_first_user():
    user = User.query.first()

    return jsonify({
        'id': user.id,
        'name': user.name,
        'age': user.age
    })

@app.route("/users/count")
def get_users_count():
    user_count = User.query.count()

    return str(user_count)

@app.route("/users")
def get_users():
    user_list = User.query.all()
    user_response = [{'id': user.id, 'name': user.name, 'age': user.age} for user in user_list]

    return jsonify(user_response)


@app.route("/users/<int:sid>")
def get_user(sid: int):
    user = User.query.get(sid)

    if user is None:
        return "User not found"

    return jsonify({
        'id': user.id,
        'name': user.name,
        'age': user.age
    })

if __name__ == '__main__':
    app.run(debug=True)


