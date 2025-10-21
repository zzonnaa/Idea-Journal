import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Idea

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ideas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/')
    def index():
        ideas = Idea.query.order_by(Idea.id.desc()).all()
        return render_template('index.html', ideas=ideas)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            tags = request.form.get('tags', '').strip()
            if not title:
                flash('Title is required', 'danger')
                return redirect(url_for('add'))
            idea = Idea(title=title, content=content, tags=tags)
            db.session.add(idea)
            db.session.commit()
            flash('Idea added', 'success')
            return redirect(url_for('index'))
        return render_template('add.html')

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete(id):
        idea = Idea.query.get_or_404(id)
        db.session.delete(idea)
        db.session.commit()
        flash('Deleted', 'success')
        return redirect(url_for('index'))

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        idea = Idea.query.get_or_404(id)
        if request.method == 'POST':
            idea.title = request.form.get('title', idea.title)
            idea.content = request.form.get('content', idea.content)
            idea.tags = request.form.get('tags', idea.tags)
            db.session.commit()
            flash('Updated', 'success')
            return redirect(url_for('index'))
        return render_template('add.html', idea=idea)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
