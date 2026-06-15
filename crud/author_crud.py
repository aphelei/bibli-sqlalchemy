from models import Book, Author, Genre, DetailsLivre
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload


def create_author(session, author_name, author_surname) -> Author:
    author = session.scalar(
        select(Author).filter_by(name=author_name, surname=author_surname)
    )
    if not author:
        author = Author(name=author_name, surname=author_surname)
        session.add(author)
        print(f"Nouvel auteur créé : {author_name} {author_surname}")

    return author


def list_authors(session):
    authors = session.scalars(
        select(Author)
        .options(selectinload(Author.books))  # one to many
        .order_by(Author.id)
    ).all()

    print("====== liste authors =============")
    if not authors:
        print("Aucun authors dans la base.")
    for author in authors:
        titres = [livre.title for livre in author.books]
        print("-", author.id, author.name, author.surname, titres)


def modify_author(session, author_id, authors_name, authors_surname):
    # stmt = update(Book).where(Book.id == book_id).values(title=book_title)
    # result = session.execute(stmt)
    author = session.get(Author, author_id)  # get utilise la/les clé primaire
    if author:
        author.name = authors_name
        author.surname = authors_surname
        return f"{authors_name} {authors_surname} updated"
    return "author id inexistant"


def delete_author(session, author_id):
    # session.execute(delete(Book).where(Book.id == book_id)) # fonctionne pas car ça cascade pas
    author = session.get(Author, author_id)

    if not author:
        return "author id inexistant"

    book_exists = session.scalar(
        select(Book).where(Book.author_id == author_id).limit(1)
    )

    if book_exists:  # author.books moins performant car ça select tout, ici si il y en a 1 je delete pas
        return f"Suppression impossible : {author.name} a encore {len(author.books)} livre(s)."

    session.delete(author)
    return f"{author.name} {author.surname} deleted"
