from typing import Generic, Type, TypeVar, Optional, List, Any
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """
    Repositorio base genérico que encapsula las operaciones CRUD
    y garantiza el manejo adecuado de sesiones y rollbacks explícitos.
    """

    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Obtiene un registro por su ID primario."""
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene una lista paginada de registros."""
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def create(self, obj: ModelType) -> ModelType:
        """Persiste una entidad en la base de datos con manejo explícito de excepciones."""
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """Actualiza un objeto existente con un diccionario de cambios."""
        try:
            for field, value in obj_in.items():
                if value is not None and hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            self.session.add(db_obj)
            self.session.commit()
            self.session.refresh(db_obj)
            return db_obj
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, id: Any) -> bool:
        """Elimina un objeto por ID."""
        try:
            db_obj = self.get_by_id(id)
            if db_obj:
                self.session.delete(db_obj)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
