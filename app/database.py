from sqlalchemy import create_engine, Column, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100), nullable=False)
    amount = Column(Float(), nullable=False)

    def __repr__(self):
        return f"expense(id={self.id}, description={self.description}, amount={self.amount})"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
