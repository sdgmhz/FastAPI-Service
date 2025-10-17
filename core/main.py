from fastapi import FastAPI, Query, status, Path, HTTPException, Form
from fastapi.responses import JSONResponse

from typing import Optional
from decimal import Decimal

app = FastAPI()

index = 3

costs_db = [
    {
        "id": 1,
        "description": "this is a description for item 1",
        "amount": 12.1,
    },
    {
        "id": 2,
        "description": "this is a description for item 2",
        "amount": 40.0,
    },
    {
        "id": 3,
        "description": "this is a description for item 3",
        "amount": 145.23,
    },
]


@app.get("/costs")
def get_cost_list(
    search: Optional[str] = Query(None, max_length=50, pattern="^[^0-9]*$")
):
    result = costs_db
    if search:
        result = [
            item
            for item in costs_db
            if search.lower() in item["description"].lower()
        ]
    for item in result:
        item["amount"] = float(item["amount"])
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@app.get("/costs/{item_id}")
def get_cost_detail(
    item_id: int = Path(description="The id of the item to get", gt=0)
):
    for item in costs_db:
        if item["id"] == item_id:
            item["amount"] = float(item["amount"])
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(
        detail="Item not found", status_code=status.HTTP_404_NOT_FOUND
    )


@app.post("/costs")
def create_cost(
    description: str = Form(min_length=3, max_length=20),
    amount: Decimal = Form(max_digits=10, decimal_places=2),
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0",
        )
    global index
    new_item = {
        "id": index + 1,
        "description": description,
        "amount": float(amount),
    }
    costs_db.append(new_item)
    if new_item:
        index += 1
    return JSONResponse(content=new_item, status_code=status.HTTP_201_CREATED)


@app.put("/costs/{item_id}")
def edit_cost(
    item_id: int,
    description: str = Form(min_length=3, max_length=20),
    amount: Decimal = Form(max_digits=10, decimal_places=2),
):
    for item in costs_db:
        if item["id"] == item_id:
            if amount <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Amount must be greater than 0",
                )
            item["description"] = description
            item["amount"] = float(amount)
            return JSONResponse(
                content=f"Item with id={item_id} updated successfully",
                status_code=status.HTTP_200_OK,
            )
    raise HTTPException(
        detail="Item not found", status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete("/costs/{item_id}")
def delete_cost(item_id: int):
    for i, n in enumerate(costs_db):
        if n["id"] == item_id:
            del costs_db[i]
            return JSONResponse(
                content={"detail": "item deleted successfully"},
                status_code=status.HTTP_204_NO_CONTENT,
            )
    raise HTTPException(
        detail="Item not found", status_code=status.HTTP_404_NOT_FOUND
    )
