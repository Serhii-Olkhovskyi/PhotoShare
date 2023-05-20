from fastapi import FastAPI
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from src.routes import photos, photo_transformer
from src.conf.config import settings

app = FastAPI()

app.include_router(photos.router, prefix='/api')
app.include_router(photo_transformer.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
