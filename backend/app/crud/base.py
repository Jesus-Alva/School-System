from typing import Any, Generic, TypeVar, Type
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ------------------------------------------------------------------
    # Lectura
    # ------------------------------------------------------------------
    def get(self, db: Session, id: int) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        # Soft delete: si el modelo tiene deleted_at, filtrar
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        return db.execute(stmt).scalar_one_or_none()

    def get_by(self, db: Session, **filtros: Any) -> ModelType | None:
        stmt = select(self.model)
        for campo, valor in filtros.items():
            stmt = stmt.where(getattr(self.model, campo) == valor)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        **filtros: Any,
    ) -> list[ModelType]:
        stmt = select(self.model)
        for campo, valor in filtros.items():
            if valor is not None:
                stmt = stmt.where(getattr(self.model, campo) == valor)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        if order_by and hasattr(self.model, order_by):
            stmt = stmt.order_by(getattr(self.model, order_by))
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def count(self, db: Session, **filtros: Any) -> int:
        stmt = select(func.count()).select_from(self.model)
        for campo, valor in filtros.items():
            if valor is not None:
                stmt = stmt.where(getattr(self.model, campo) == valor)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        return db.execute(stmt).scalar_one()

    def exists(self, db: Session, **filtros: Any) -> bool:
        return self.get_by(db, **filtros) is not None

    # ------------------------------------------------------------------
    # Escritura
    # ------------------------------------------------------------------
    def create(self, db: Session, obj_in: CreateSchemaType | dict) -> ModelType:
        data = obj_in.model_dump() if isinstance(obj_in, BaseModel) else obj_in
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict,
    ) -> ModelType:
        data = (
            obj_in.model_dump(exclude_unset=True)
            if isinstance(obj_in, BaseModel)
            else obj_in
        )
        for campo, valor in data.items():
            setattr(db_obj, campo, valor)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int, soft: bool = True) -> ModelType | None:
        db_obj = self.get(db, id)
        if not db_obj:
            return None
        if soft and hasattr(db_obj, "deleted_at"):
            from datetime import datetime, timezone

            db_obj.deleted_at = datetime.now(timezone.utc)
        else:
            db.delete(db_obj)
        db.commit()
        return db_obj
