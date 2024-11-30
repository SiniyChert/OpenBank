from fastapi import FastAPI
from contextlib import asynccontextmanager
import dbRequests as dbr
from routers.users_router import router as userRouter
from routers.credit_router import router as creditRouter
from routers.transactions_router import router as transactionsRouter
from routers.taxes_router import router as taxesRouter

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Жизненный цикл приложения. Всё до yield выполняется при запуске программы, всё что после - при завершении работы
    print("===APP SETUP===")
    if not dbr.connectToDB():
        print("db connection - failed")
    print("db connection - success")
    yield
    print("bye-bye")


app = FastAPI(lifespan=lifespan)
app.include_router(userRouter)
app.include_router(creditRouter)
app.include_router(transactionsRouter)
app.include_router(taxesRouter)


@app.get("/ping/")
def ping():
    return {
        "responce": "pong",
    }
