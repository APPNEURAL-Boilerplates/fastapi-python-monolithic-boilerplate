from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from app.common.responses import success_response
from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def list_users(request: Request, service: UserService = Depends(get_user_service)) -> JSONResponse:
    users = [UserResponse.model_validate(user) for user in service.list_users()]
    return success_response(request, data=users)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    request: Request,
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    user = service.create_user(payload)
    return success_response(
        request,
        data=UserResponse.model_validate(user),
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/{user_id}")
def get_user(
    request: Request,
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    user = service.get_user(user_id)
    return success_response(request, data=UserResponse.model_validate(user))


@router.patch("/{user_id}")
def update_user(
    request: Request,
    user_id: str,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    user = service.update_user(user_id, payload)
    return success_response(request, data=UserResponse.model_validate(user))


@router.delete("/{user_id}")
def delete_user(
    request: Request,
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    service.delete_user(user_id)
    return success_response(request, data={"deleted": True})
