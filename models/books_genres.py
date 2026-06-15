#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:33:08 2026

@author: aphe
"""

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class BooksGenres(Base):  # table de liaison
    __tablename__ = "books_genres"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id"), primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genre.id"), primary_key=True
    )
