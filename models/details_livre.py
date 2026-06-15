#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:32:10 2026

@author: aphe
"""

from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book


class DetailsLivre(Base):
    __tablename__ = "details_livre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resume: Mapped[str] = mapped_column(nullable=True)
    nb_pages: Mapped[int] = mapped_column()

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), unique=True)
    book: Mapped["Book"] = relationship(back_populates="details")

    def __repr__(self):
        return f"<DetailsLivre(id={self.id}, resume='{self.resume}', nb_pages={self.nb_pages})>"
