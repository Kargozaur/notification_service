from . import APIRouter, Depends, status, Response
from dependancies.user_dependancy import get_user_service
from schemas.schemas import CreateUser, LoginUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signin", status_code=status.HTTP_200_OK)
async def user_signin(
    user_credential: CreateUser,
    user_service=Depends(get_user_service),
):
    await user_service.create_user(user_credential)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/login")
async def user_login(
    user_credential: LoginUser, user_service=Depends(get_user_service)
):
    user = await user_service.login_user(user_credential)
    return user
