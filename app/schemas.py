from pydantic import BaseModel, Field, field_validator


class BaseExpenseSchema(BaseModel):
    """base schema for expense data"""
    description: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)

    @field_validator("description")
    @classmethod
    def validation_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("description can not be empty")
        return value


class ExpenseCreateSchema(BaseExpenseSchema):
    """schema for creating an expense"""
    pass


class ExpenseUpdateSchema(BaseExpenseSchema):
    """schema for updating an expense"""
    pass


class ExpenseResponseSchema(BaseExpenseSchema):
    """Schema for returning an expense."""
    id: int
