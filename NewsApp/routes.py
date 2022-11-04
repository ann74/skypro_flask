from app import app, db
from flask import render_template, redirect
from forms import CategoryForm, NewsForm
from models import News, Category


@app.route('/')
def index():
    return render_template('index.html', title='News App')


@app.route('/news')
def news_page():
    news = News.query.all()
    return render_template('news_page.html', news=news)


@app.route('/news/add', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    form.category_id.choices = [(c.id, c.name) for c in db.session.query(Category).all()]
    if form.validate_on_submit():
        new = News(
            title=form.title.data,
            text=form.text.data,
            is_published=form.is_published.data,
            category_id=form.category_id.data
        )
        db.session.add(new)
        db.session.commit()
        return redirect('/news')
    return render_template('add_news.html', form=form)


@app.route('/news/<int:news_id>')
def curr_news(news_id):
    res = News.query.get(news_id)
    return render_template('news.html', res=res)


@app.route('/news/<int:news_id>/edit', methods=['GET', 'POST'])
def edit_news(news_id):
    res = News.query.get(news_id)
    form = NewsForm(
        title=res.title,
        text=res.text,
        category_id=res.category_id,
        is_published=res.is_published
    )
    form.category_id.choices = [(c.id, c.name) for c in db.session.query(Category).all()]
    if form.validate_on_submit():
        res.title = form.title.data
        res.text = form.text.data
        res.is_published = form.is_published.data
        res.category_id = form.category_id.data
        db.session.add(res)
        db.session.commit()
        return redirect(f'/news/{res.id}')
    return render_template('add_news.html', form=form)


@app.route('/news/<int:news_id>/delete')
def delete_news(news_id):
    res = News.query.get(news_id)
    db.session.delete(res)
    db.session.commit()
    return redirect('/news')


@app.route('/news/categories')
def categories():
    category_names = db.session.query(Category).all()
    return render_template('category.html', category_names=category_names)


@app.route('/news/categories/add', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, is_published=form.is_published.data)
        db.session.add(category)
        db.session.commit()
        return redirect('/news/categories')
    return render_template('add_cat.html', form=form)


@app.route('/news/categories/<category>')
def category_news(category):
    our_category = Category.query.filter(Category.name == category).first()
    res = News.query.filter(News.category_id == our_category.id).all()
    return render_template('news_page.html', news=res)


if __name__ == '__main__':
    app.run(debug=True)
