from fastapi import APIRouter
import dbRequests as dbr
from schemas import User, UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def getUser(
    id: int | None = None, username: str | None = None, FIO: str | None = None
) -> UserSchema | None:
    res = dbr.getUser(id, username, FIO)
    if res is not None:
        return UserSchema.from_user(res)
    else:
        return None


@router.post("/{id}")
async def setUserStats(
    id: int, balance: int | None = None, isBanned: bool | None = None
) -> UserSchema | None:
    pass


@router.get("/find")
async def findUser(pattern: str) -> list[UserSchema]:
    pattern = pattern.lower()
    res = dbr.findUser(pattern)
    responce = [UserSchema.from_user(i) for i in res]
    return responce
