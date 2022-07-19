from fastapi import Depends, FastAPI

from routers.users import router


app = FastAPI(dependencies=[])


app.include_router(router)



