from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)
CORS(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(800))
    image = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=False)


@app.route("/article")
@app.route("/article/<id>")
def article(id=-1):
    if id == -1:
        articles = Article.query.all()
    else:
        articles = [Article.query.get(id)]
    return_data = []
    for article in articles:
        return_data.append(
            {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'image': article.image,
                'category': article.category
            })
    if id != -1:
        return jsonify(return_data[0])

    return jsonify(return_data)

# need to post a json like this one:
# {
#     "category": "News",
#     "content": "Hello this is content",
#     "image": "https://picsum.photos/id/139/300/300",
#     "title": "News 888888 is here"
#   }
@app.route('/create_article/<id>', methods=['POST'])
@app.route('/create_article', methods=['POST'])
def create_article(id=-1):
    data = request.get_json()    
    # add new article
    if id==-1:
        new_article = Article(title=data['title'], content=data['content'], category=data['category'],image=data['image'])
        db.session.add(new_article)
        db.session.commit()
        return jsonify({'message': 'Article created successfully'})
    else:
    # update article
        article = Article.query.get(id)
        article.title = data['title']
        article.content = data['content']
        article.category = data['category']
        article.image = data['image']
        db.session.commit()
        return jsonify({'message': 'Article updated successfully'})

@app.route('/')
def index():
    return """
    <h3>This is a back end News article api</h3>
    <br> <h4>Endpoints you can use are: <h4>
    <ul>
    <br><li> /article (GET)</li>
    <br> <li> /article/id (GET)</li>
    <br> <li> /create_article (POST)</li>
    <br> <li> /delete_article (DELETE)</li>
    """

@app.route('/delete_article/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get(id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    else:
        return jsonify({'message': f'Error deleting {id}'})


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
