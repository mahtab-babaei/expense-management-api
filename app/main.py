from fastapi import FastAPI, status, Body, Path, HTTPException, Response, Query
from fastapi.responses import JSONResponse

app = FastAPI()

expenses = {
    1: {"id": 1, "description": "groceries", "amount": 125.5},
    2: {"id": 2, "description": "taxi", "amount": 25.85},
    3: {"id": 3, "description": "Clothing", "amount": 406.65},
    4: {"id": 4, "description": "bills", "amount": 32.3},
    5: {"id": 5, "description": "coffee", "amount": 9.99},
}


@app.get("/expenses")
def retrieve_all_costs(q: str | None = Query(alias="Search in descriptions", default=None)):
    result = expenses
    if q:
        result = [item for item in expenses.values() if q.lower(
        ) in item["description"].lower()]
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@app.post("/expenses")
def create_new_cost(description: str = Body(), amount: float = Body()):
    if not description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="description can not be empty")
    new_id = max(expenses.keys()) + 1
    new_cost = {
        "id": new_id,
        "description": description,
        "amount": amount
    }
    expenses[new_id] = new_cost
    return JSONResponse(content=new_cost, status_code=status.HTTP_201_CREATED)


@app.get("/expenses/{expense_id}")
def retrieve_cost(expense_id: int = Path(description="The ID of the expense")):
    expense = expenses.get(expense_id)
    if expense:
        return JSONResponse(content=expense, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")


@app.put("/expenses/{expense_id}")
def update_cost(expense_id: int, description: str = Body(), amount: float = Body()):
    expense = expenses.get(expense_id)
    if expense:
        if not description.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="description can not be empty")
        expense["description"] = description
        expense["amount"] = amount
        return JSONResponse(content=expense, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")


@app.delete("/expenses/{expense_id}")
def remove_cost(expense_id: int):
    expense = expenses.get(expense_id)
    if expense:
        expenses.pop(expense_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")
