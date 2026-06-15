from models.base import get_db_session, init_db
from models import Book, Author, Genre, DetailsLivre
import crud
from sqlalchemy import select, func
from sqlalchemy.orm import Session

"""
Hormis l'indexation maladroite [0] dans create_author, tout est fonctionnel et
solide ! Tu as construit une excellente base (bien structurée) sur laquelle
venir brancher une interface terminal (input() classiques, librairie Rich, ou
Textual), ou même une future API web (FastAPI/Flask).
"""


def create_sample_data(session: Session):
    print("Insertion des données de test...")

    genre1 = Genre(genre="police")
    genre2 = Genre(genre="classique")
    session.add(genre1)

    book1 = Book(title="Germinal")
    book1.genres.append(genre2)

    author1 = Author(name="Hugo", surname="Victor")
    author2 = Author(name="Zola", surname="Zola")
    session.add_all([author1, author2])

    author2.books.append(book1)


if __name__ == "__main__":
    init_db(delete=False)

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

        crud.modify_book(session, 3, "le titre")

        crud.list_books(session)

        crud.list_authors(session)
