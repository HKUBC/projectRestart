from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.models.items.categories_table import categories
from pydantic import BaseModel, ConfigDict

class CreateCategory(BaseModel):
    category: str

class CategoryResponse(BaseModel):
    id: int
    category: str
model_config = ConfigDict(from_attributes=True)

def is_empty(db: Session = Depends(get_db)):
    query = categories.select()
    result = db.execute(query).scalars().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Category does not exist!")


router = APIRouter()

# Get categories by ID
@router.get("/{id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
def get_category (id : str, db1= Depends(get_db)):

    is_empty(db1)
    #check if category exists
    
    query = categories.select().where((categories.c.id == id) & (categories.c.deleted_at.is_(None)))
    result= db1.execute(query).first()
    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Category {id} doesn't exists")
    return result
    
@router.get("", status_code= status.HTTP_200_OK)
def get_categories(db1: Session = Depends(get_db)):
    query = categories.select().where(categories.c.deleted_at.is_(None)).with_only_columns(
        categories.c.id,
        categories.c.category
    )
    result = db1.execute(query).mappings().all()
    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No categories exist yet!")
    return result

@router.post("", response_model= CreateCategory,status_code=status.HTTP_201_CREATED)
def create_category(add_cat: CreateCategory, db1: Session = Depends(get_db)):
    
    query = categories.select().where((categories.c.category == add_cat.category)& categories.c.deleted_at.is_(None))
    result= db1.execute(query).first()
    if result:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f"Category {add_cat.category} already exists")
    query_add = categories.insert().values(
        category = add_cat.category  
    ).returning(categories.c.category)
    addToDB = db1.execute(query_add).mappings().all()
    db1.commit()
    return addToDB



    