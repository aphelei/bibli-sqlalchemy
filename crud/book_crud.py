from models import Book, Author, Genre, DetailsLivre
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload, selectinload


def create_book(
    session, book_title, book_author, book_details, book_genres
) -> Book:
    author = session.scalar(
        select(Author).filter_by(name=book_author[0], surname=book_author[1])
    )
    if not author:
        author = Author(name=book_author[0], surname=book_author[1])
        session.add(author)
        print(f"Nouvel auteur créé : {book_author[0]}")

    existing_book = session.scalar(
        select(Book).filter_by(title=book_title, author_id=author.id)
    )

    if existing_book:
        print(f"Le livre '{book_title}' existe déjà pour cet auteur.")
        return

    book = Book(title=book_title, author=author)

    session.add(book)

    details = DetailsLivre(resume=book_details[0], nb_pages=book_details[1])
    book.details = details

    for g in book_genres:
        genre = session.scalar(select(Genre).filter_by(genre=g))
        if not genre:
            print(f"nouveau genre créé : {g}")
            genre = Genre(genre=g)
        book.genres.append(genre)

    return book


def list_books(session):  # pagination avec select(Book).limit(10).offset(20)
    """
        select(Book).join(Author)	        SELECT ... FROM book JOIN author ON ... (Utilisé pour filtrer/trier, mais ne remplit pas l'objet auteur)
        options(joinedload(Book.author))	    SELECT book.*, author.* FROM book JOIN author ON ... (Utilisé pour remplir l'objet book.author)
        options(selectinload(Book.genres))	SELECT * FROM book; <br> puis <br> SELECT * FROM genre WHERE book_id IN (...);

    ex: joinedload (1:1 et N:1). mettre .unique avant .all
        multiplication des données sur :N (si 1 auteur a 10 livres, ça renvoie 10 lignes au lieu de 1)
                                            si 10 livres ont 2 tags ça renvoie 20 lignes au lieu de 10

    ex: selectinload (1:N et N:N) : pas de multiplication des données (on demande 10 lignes, on a 10 lignes)

    """
    books = session.scalars(
        select(Book)
        .options(
            joinedload(Book.details),  # one to one
            joinedload(Book.author),  # many to one
            selectinload(Book.genres),  # many to many
        )
        .order_by(Book.id)
    ).all()

    print("====== liste livres =============")
    if not books:
        print("Aucun livre dans la base.")
    for book in books:
        pages = book.details.nb_pages if book.details else "N/A"
        resume = book.details.resume if book.details else "N/A"
        # print(book)
        print(
            f"- {book.id} {book.title} ({book.author.name}) : {[g.genre for g in book.genres]} : {pages} pages : {resume}"
        )
    print(books[-1])


def modify_book(session, book_id, book_title):
    # stmt = update(Book).where(Book.id == book_id).values(title=book_title)
    # result = session.execute(stmt)
    book = session.get(Book, book_id)  # get utilise la/les clé primaire
    if book:
        book.title = book_title
        return f"{book_title} updated"
    return "book id inexistant"


def delete_book(session, book_id):
    # session.execute(delete(Book).where(Book.id == book_id)) # fonctionne pas car ça cascade pas
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        return f"{book.title} deleted"
    return "book id inexistant"


def search_book(session, title, author):
    pass


# Rechercher un livre avec un mot-clé (ex: select(Book).where(Book.title.ilike('%mot%'))).
