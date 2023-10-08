from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys


sys.path.append("..")


from backend.products.router import router as products_router
from backend.auth.router import router as users_router


origins = [
    '127.0.0.1:3000',
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(users_router)




