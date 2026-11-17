from fastapi import FastAPI, status, Path, HTTPException, Response, Query, Depends
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema
from database import get_db, Expense
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/expenses", response_model=list[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
def retrieve_all_costs(q: str | None = Query(alias="Search in descriptions", default=None), db: Session = Depends(get_db)):
    query = db.query(Expense)
    if q:
        query = query.filter(Expense.description.ilike(f"%{q}%"))
    result = query.all()
    return result


@app.post("/expenses", response_model=ExpenseResponseSchema, status_code=status.HTTP_201_CREATED)
def create_new_cost(request: ExpenseCreateSchema, db: Session = Depends(get_db)):
    new_cost = Expense(description=request.description, amount=request.amount)
    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)
    return new_cost


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def retrieve_cost(expense_id: int = Path(gt=0), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item not found")
    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def update_cost(expense_id: int, expense_data: ExpenseUpdateSchema, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    expense.description = expense_data.description
    expense.amount = expense_data.amount
    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cost(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    db.delete(expense)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
