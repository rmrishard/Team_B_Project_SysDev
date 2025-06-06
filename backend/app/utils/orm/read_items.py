from sqlmodel import Session, select, Field, SQLModel
from typing import Optional
from app import engine # works when deployed false error reported by PyCharm IDE

class ReadItems:

    @classmethod
    def read(cls,model_type, modifier_fn=None):
        if not modifier_fn:
            return cls.all(model_type)
        else:
            return cls.all_with(model_type, modifier_fn)

    @classmethod
    def all(cls,model_type):
        with Session(engine) as session:
            statement = select(model_type)
            results = session.exec(statement).all()
            return results
        return None

    @classmethod
    def all_with(cls,model_type, modifier_fn):
        with Session(engine) as session:
            statement = select(model_type)
            statement = modifier_fn(statement)
            results = session.exec(statement).all()
            return results
        return None


    @classmethod
    def with_id(cls, model_type, id):
        with Session(engine) as session:
            statement = select(model_type).where(model_type.getIdField() == id)
            result = session.exec(statement).one_or_none() #There should only be one match according to id
            return result
        return None