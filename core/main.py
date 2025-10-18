from fastapi import FastAPI, Query, status, Path, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List


from schemas import CostResponseSchema, CostCreateSchema, CostUpdateSchema


app = FastAPI()

index = 3

costs_db = [
    {
        "id": 1,
        "description": "this is a description for item 1",
        "amount": 12.1,
        "email": "cost1@example.com",
    },
    {
        "id": 2,
        "description": "this is a description for item 2",
        "amount": 40.0,
        "email": "cost2@example.com",
    },
    {
        "id": 3,
        "description": "this is a description for item 3",
        "amount": 145.23,
        "email": "cost2@example.com",
    },
]


@app.get("/costs", response_model=List[CostResponseSchema], status_code=status.HTTP_200_OK)
def get_cost_list(search: Optional[str] = Query(None, max_length=50, pattern="^[^0-9]*$")):
    result = costs_db
    if search:
        result = [item for item in costs_db if search.lower() in item["description"].lower()]
    return result


@app.get("/costs/{item_id}", response_model=CostResponseSchema, status_code=status.HTTP_200_OK)
def get_cost_detail(item_id: int = Path(description="The id of the item to get", gt=0)):
    for item in costs_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(detail="Item not found", status_code=status.HTTP_404_NOT_FOUND)


@app.post("/costs", response_model=CostResponseSchema, status_code=status.HTTP_201_CREATED)
def create_cost(cost: CostCreateSchema):
    global index
    cost_obj = {
        "id": index + 1,
        "description": cost.description,
        "amount": cost.amount,
    }
    if cost_obj:
        index += 1
    costs_db.append(cost_obj)
    return cost_obj


@app.put("/costs/{item_id}", response_model=CostResponseSchema, status_code=status.HTTP_200_OK)
def edit_cost(item_id: int, cost: CostUpdateSchema):
    for item in costs_db:
        if item["id"] == item_id:
            item["description"] = cost.description
            item["amount"] = cost.amount
            return item
    raise HTTPException(detail="Item not found", status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/costs/{item_id}")
def delete_cost(item_id: int):
    for i, n in enumerate(costs_db):
        if n["id"] == item_id:
            del costs_db[i]
            return JSONResponse(
                content={"detail": "item deleted successfully"},
                status_code=status.HTTP_204_NO_CONTENT,
            )
    raise HTTPException(detail="Item not found", status_code=status.HTTP_404_NOT_FOUND)
