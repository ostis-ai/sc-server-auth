from fastapi import FastAPI
import auth, admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
