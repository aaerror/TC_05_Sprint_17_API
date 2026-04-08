from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import BaseModel, Field

from typing import Annotated


router = APIRouter(prefix="/estimator", tags=["Machine Learning"])

# schemas
class Predict(BaseModel):
    username: str
    email: str




@router.post(
    "/",
    summary="Make a new estimation",
    status_code=status.HTTP_200_OK
)
def estimate(request: Annotated[dict, Depends(Predict)]):
    print(request)

    return {
        "msg": "Making a new predict"
    }

@router.get("/", summary="Get model info", status_code=200)
def get_user():
    return {
        "msg": "Model info retrieved"
    }
