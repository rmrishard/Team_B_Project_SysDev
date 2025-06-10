from sqlmodel import Session, select, Field, SQLModel
from fastapi import HTTPException
from typing import Optional
from app import engine # works when deployed false error reported by PyCharm IDE

class UpdateItems:

    @classmethod
    def with_id(cls, model_type, user_model_data, id):
        with Session(engine) as session:
            statement = select(model_type).where(model_type.getIdField() == id)
            db_item = session.exec(statement).one_or_none()  # There should only be one match according to id

            if not db_item:
                raise HTTPException(status_code=404, detail=f"{model_type.getName()} not found")

            user_item_data = user_model_data.model_dump(exclude_unset=True)
            db_item.sqlmodel_update(user_item_data)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        return None