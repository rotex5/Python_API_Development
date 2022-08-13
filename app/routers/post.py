from typing import List, Optional
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user), 
        limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #to get all posts regardless of who is loggeg in
    #print(search)
    #print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
            models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(search)
    #functionality gets posts for a specific user that is logged in
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).all()

    #print(current_user.email)
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(posts)
    #return posts
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    #print(current_user.id)
    #print(current_user.email)

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    #scalable solution to the one below

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #the above method is not scalable
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #               (post.title, post.content, post.published))

    #new_post = cursor.fetchone()
    #conn.commit()
    return new_post

#@router.get("/{id}", response_model=schemas.PostResponse)  #path/path parameter
@router.get("/{id}", response_model=schemas.PostOut)  #path/path parameter
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
            models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    #functionality gives access to posts created by you only
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                    detail= "Note authorized to perform requested action")


    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):

    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist" )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail= "Note authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, (str(id),)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist" )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail= "Note authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session= False)
    #scalable solution to the one below

    #post_query.update({'title': 'hey this is my update tile', 'content': 'this is my updated content'},
    #       synchronize_session = False)
    #the code above works but its hard coded.
    db.commit()

    return post_query.first()

