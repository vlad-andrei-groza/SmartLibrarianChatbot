from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router
from app.routes import text_to_speech

app = FastAPI(title="Book Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"ok": True}


app.include_router(search_router)
app.include_router(chat_router)
