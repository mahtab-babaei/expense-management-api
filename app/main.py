from fastapi import FastAPI, status, Path, HTTPException, Response, Query
from schemas import ExpenseResponseSchema, ExpenseCreateSchema, ExpenseUpdateSchema

app = FastAPI()

expenses = {
    1: {"id": 1, "description": "groceries", "amount": 125.5},
    2: {"id": 2, "description": "taxi", "amount": 25.85},
    3: {"id": 3, "description": "Clothing", "amount": 406.65},
    4: {"id": 4, "description": "bills", "amount": 32.3},
    5: {"id": 5, "description": "coffee", "amount": 9.99},
}


@app.get("/expenses", response_model=list[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
def retrieve_all_costs(q: str | None = Query(alias="Search in descriptions", default=None)):
    result = list(expenses.values())
    if q:
        result = [item for item in result if q.lower(
        ) in item["description"].lower()]
    return result


@app.post("/expenses", response_model=ExpenseResponseSchema, status_code=status.HTTP_201_CREATED)
def create_new_cost(expense: ExpenseCreateSchema):
    new_id = max(expenses.keys(), default=0) + 1
    new_cost = {
        "id": new_id,
        "description": expense.description,
        "amount": expense.amount,
    }
    expenses[new_id] = new_cost
    return new_cost


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def retrieve_cost(expense_id: int = Path(gt=0)):
    expense = expenses.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item not found")
    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def update_cost(expense_id: int, expense_data: ExpenseUpdateSchema):
    expense = expenses.get(expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    expense["description"] = expense_data.description
    expense["amount"] = expense_data.amount
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cost(expense_id: int):
    expense = expenses.get(expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    expenses.pop(expense_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
