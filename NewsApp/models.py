from app import db, app


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=True)

    news = db.relationship('News', backref='category', lazy='dynamic')

    # def __repr__(self):
    #     return f'{self.name}'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_published = db.Column(db.Boolean, default=True)

    # def __repr__(self):
    #     return f'{self.title} - {self.text}'


def inert_news():
    news1 = News(
        title='Telegram запустил продажу никнеймов за Toncoin',
        text='Telegram запустил Fragment — платформу для продажи никнеймов для мессенджера. Выставленные на аукцион '
             'свободные ники продаются за Tonkoin (TON). На текущий момент самый дорогой ник в списке — casino. Его '
             'стоимость составляет 52,5 тыс TON или ₽6,19 млн. В списке платформы находятся все зарегистрированные '
             'имена, даже тех, кто активно пользуется Telegram. Однако никнеймы активных пользователей не выставлены '
             'на аукцион.',
        category_id=1,
        is_published=True)

    with app.app_context():
        db.session.add(news1)
        db.session.commit()


if __name__ == '__main__':
    inert_news()
