# -*- coding: utf-8 -*-
"""
Database module.

Includes the SQLAlchemy database object and DB-related utilities
"""
from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship

from .extensions import db

# Alias common SQLAlchemy names
Boolean = db.Boolean
Column = db.Column
DateTime = db.DateTime
ForeignKey = db.ForeignKey
Integer = db.Integer
String = db.String
association_proxy = association_proxy
backref = backref
func = func
relationship = relationship
session = db.session


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """
    Primary key mixin.

    A mixin that adds a surrogate integer 'primary key' column named ``id`` to
    any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
