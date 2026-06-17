from markupsafe import escape
from flask import Flask, url_for, request, render_template, redirect
from models.base import get_db_session, init_db
from models import Book, Author, Genre
from sqlalchemy import select, func
from sqlalchemy.orm import Session
import crud


def create_sample_data(session: Session):
    print("Insertion des données de test...")

    genre1 = Genre(genre="police")
    genre2 = Genre(genre="classique")
    genre3 = Genre(genre="Science-fiction")
    session.add_all([genre1, genre2, genre3])

    book1 = Book(title="Germinal")
    book2 = Book(title="Au Bonheur des Dames ")
    book3 = Book(title="L'oeuvre")
    book1.genres.append(genre2)
    book2.genres.append(genre2)
    book3.genres.append(genre2)

    book4 = Book(title="Fondation 1")
    book5 = Book(title="Fondation 2")
    book4.genres.append(genre3)
    book5.genres.append(genre3)


    author1 = Author(name="Hugo", surname="Victor")
    author2 = Author(name="Zola", surname="Emile")
    author3 = Author(name="Baudelaire", surname="Charles")
    author4 = Author(name="Azimov", surname="Isaac")
    session.add_all([author1, author2, author3, author4])

    author2.books.append(book1)
    author2.books.append(book2)
    author2.books.append(book3)
    author4.books.append(book4)
    author4.books.append(book5)



if __name__ == "__main__":
    init_db(delete=True)

    with get_db_session() as session:
        session: Session
    
        # books = session.scalars(select(Book))  # .all() donne une liste
        # print([book.title for book in books])
        # book_count = session.execute(
        #     func.count(Author.id)
        # ).scalar_one_or_none()
        book_count = session.scalar(select(func.count(Author.id)))
        # book_count = session.scalars(select(func.count(Author.id)))
        # book_count = book_count.one()

        if not book_count:
            create_sample_data(session)
        else:
            print(f"Base déjà remplie ({book_count} auteurs trouvés).")

        # zola = session.execute(
        #     select(Author).filter_by(name="Zola")
        # ).scalar_one()

        # print(f"Auteur : {zola.name}")
        # print(f"Nombre de livres : {len(zola.books)}")
        # for livre in zola.books:
        #     print(f" - Titre du livre : {livre.title}")

        # genre_police = session.execute(
        #     select(Genre).where(Genre.genre == "police")
        # ).scalar_one()
        # print(genre_police.genre)

        # germinal = session.execute(
        #     select(Book).where(Book.title == "Germinal")
        # ).scalar_one()
        # germinal.genres.append(genre_police)

        book_add = crud.create_book(
            session,
            "tata7",
            ["ndddd", "surname"],
            ["résumé", 1],
            ["police", "classique"],
        )
        # crud.list_books(session)

        # print(crud.modify_book(session, 8, "eeeeeeeeeeeeeeee"))
        # crud.list_books(session)
        # print(crud.delete_book(session, 13))

        # crud.modify_book(session, 3, "le titre")

        crud.list_books(session)

        crud.list_authors(session)
    app = Flask(__name__)

    @app.route('/')
    def index():
        return redirect(url_for('login_get'))

    # @app.get('/login')
    # def login_get():
    #     return "afficher login form"

    # @app.post('/login')
    # def login_post():
    #     return "serveur fait la connexion"
    
    # def valid_login(u, p):
    #     if u == 'u' and p == 'p':
    #         return True
    #     return False
    # def log_the_user_in(u):
    #     return "logged in"
    # @app.route('/login', methods=['POST', 'GET'])
    # def login():
    #     error = None
    #     if request.method == 'POST':
    #         if valid_login(request.form['username'],
    #                     request.form['password']):
    #             return log_the_user_in(request.form['username'])
    #         else:
    #             error = 'Invalid username/password'
    #     # the code below is executed if the request method
    #     # was GET or the credentials were invalid
    #     return render_template('login.html', error=error)
    
    @app.get('/login/')
    def login_get():
        return render_template('login.html')

    @app.post('/login/validation')
    def login_post():
        username = request.form.get('username')
        password = request.form.get('password')
    
        return f"Le serveur fait la connexion pour l'utilisateur : {username} avec {password}"

    # @app.route('/list', methods=['POST', 'GET'])
    # def list_books():
    #     if request.method == 'GET':
    #         return render_template('list_items.html', method='get')
    #     else:
    #         books = crud.list_books(session)
    #         return render_template('list_items.html', liste_livres=books)
    
    @app.route('/list', methods=['GET', 'POST'])
    def list_items():
        type_item = request.form.get('type_item')
        # type_item = request.args.get('type_item') # avec argument ?arg=value
        if type_item == 'books':
            items_trouves = ['books']
            items_trouves.extend(crud.list_books(session))
        elif type_item == 'authors':
            items_trouves = ['authors']
            items_trouves.extend(crud.list_authors(session))
        else:
            return render_template('hello.html')
        return render_template('list_items.html', items=items_trouves)
    
    @app.route('/search', methods=['GET']) # <int:item_id>
    def search_item(): # ne pas mettre le paramètre ici sinon request.args.get peut pas le prendre
        # mettre un arg si app.route /search/id
        id_item = request.args.get('id_item')
        type_item = request.args.get('type_item')
        print(crud.list_authors(session))
        if type_item == 'book':
            item = crud.search_book(session, id_item)
        elif type_item == 'author':
            print(crud.search_author(session, id_item))
            item = crud.search_author(session, id_item)
        else:
            return render_template('hello.html')
        return render_template('search_item.html', item=item, type_item=type_item)    
    print(crud.list_authors(session))
    # @app.route('/list/<items>', methods=['GET', 'POST'])
    # def list_items(items): # url_for("list_items", items='books')
    #     # La variable "items" vient directement de l'URL maintenant !
    #     if items == 'books':
    #         items_trouves = crud.list_books(session)
    #     elif items == 'authors':
    #         items_trouves = crud.list_authors(session)
    #     else:
    #         return render_template('hello.html')
            
    #     return render_template('list_items.html', items=items_trouves)
    
    # def list_authors():
    #     if request.method == 'GET':
    #         return render_template('list_items.html', method='get')
    #     else:
    #         authors = crud.list_authors(session)
    #         return render_template('list_items.html', liste_livres=authors)
    
    

    @app.route('/user/<username>')
    def profile(username):
        return f'{username}\'s profile'
    
    # @app.route("/hello")
    # def hellooooo():
    #     name = request.args.get("name", "Flask")
    #     return f"Hello, {escape(name)}!"

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', person=name)

    # with app.test_request_context():
    #     print(url_for('index'))
    #     # print(url_for('login'))
    #     # print(url_for('login', next='/'))
    #     print(url_for('hello'))
    #     print(url_for('profile', username='John Doe'))

    app.run()
