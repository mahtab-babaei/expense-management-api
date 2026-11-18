from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class ExpenseModel(Base):
    __tablename__ = "expenses"

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100), nullable=False)
    amount = Column(Float(), nullable=False)

    def __repr__(self):
        return f"expense(id={self.id}, description={self.description}, amount={self.amount})"
