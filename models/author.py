#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:29:54 2026

@author: aphe
"""

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', surname='{self.surname}')>"
