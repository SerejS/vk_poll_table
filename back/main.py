import asyncio

import uvicorn as uvicorn
from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from back.vk_requests import get_poll_answers, get_poll_lessons
from back.utils import get_students_from_file

# Setup FastAPI
app = FastAPI()

app.mount('/static',
          StaticFiles(directory='../front/build/static', html=True), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="../front/build")

async def main():
    config = uvicorn.Config("main:app", port=7139, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

# Endpoints
@app.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/lessons")
async def get_lessons(owner_id, poll_id):
    answers = get_poll_answers(owner_id, poll_id)
    lessons = get_poll_lessons(owner_id, poll_id, answers)
    return lessons

@app.get("/students")
async def get_students():
    return get_students_from_file()

