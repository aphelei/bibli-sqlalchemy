#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:26:14 2026

@author: aphe
"""

from .base import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .author import Author
    from .genre import Genre
    from .details_livre import DetailsLivre


class Book(Base):
    __tablename__ = "book"
    __table_args__ = (
        UniqueConstraint("title", "author_id", name="uq_book_title_author"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    # books-author -> many to one : clé étrangère du côté many + relationship des 2 côtés
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
    # book-details -> one to one : clé étrangère d'un côté avec unique=True + relationship des 2 côtés
    details: Mapped["DetailsLivre"] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
    # books-genres -> many to many : relationship avec secondary=table_liaison
    genres: Mapped[list["Genre"]] = relationship(
        secondary="books_genres", back_populates="books"
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author={self.author}, details={self.details}, genres={self.genres})>"
