from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import noticia as crud_noticia
from app.schemas.noticia import NoticiaRead

router = APIRouter(prefix="/publico", tags=["Sitio público"])


@router.get("/noticias", response_model=list[NoticiaRead])
def noticias(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud_noticia.list_publicadas(db, skip=skip, limit=limit)


@router.get("/noticias/{slug}", response_model=NoticiaRead)
def noticia_detalle(slug: str, db: Session = Depends(get_db)):
    from app.core.exceptions import NotFoundError

    noticia = crud_noticia.get_by_slug(db, slug)
    if not noticia or not noticia.publicado:
        raise NotFoundError("Noticia no encontrada")
    return noticia
