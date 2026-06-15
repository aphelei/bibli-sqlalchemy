#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:31:22 2026

@author: aphe
"""

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .book import Book


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    genre: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(
        secondary="books_genres", back_populates="genres"
    )

    def __repr__(self):
        return f"<Genre(id={self.id}, genre={self.genre})>"
