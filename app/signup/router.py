from fastapi import APIRouter

signup_router = APIRouter()


@signup_router.post("/new_user")
def new_user():
    pass
