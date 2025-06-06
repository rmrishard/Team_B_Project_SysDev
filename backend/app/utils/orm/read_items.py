from sqlmodel import Session, select, Field, SQLModel
from typing import Optional
from app import engine # works when deployed false error reported by PyCharm IDE

class ReadItems:

    @classmethod
    def read(cls,model_type, params=None):
        if not params:
            return cls.all(model_type)
        return None

    @classmethod
    def all(cls,model_type):
        with Session(engine) as session:
            statement = select(model_type)
            results = session.exec(statement).all()
            return results
        return None

    @classmethod
    def with_id(cls, model_type, id):
        with Session(engine) as session:
            statement = select(model_type).where(model_type.getIdField() == id)
            result = session.exec(statement).one() #There should only be one match according to id
            return result
        return None