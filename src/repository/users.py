from sqlalchemy.orm import Session

from src.database.models import User


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()
