import asyncio
import json
import os

import uvicorn as uvicorn
from fastapi import FastAPI, Request

import requests as requests
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware


def get_students_from_file():
    file = open("students.json", 'r', encoding='utf-8')
    students = json.loads(file.read())
    file.close()
    return students


class Lesson:
    def __init__(self, lesson_id, name, student_ids):
        self.id = lesson_id
        self.name = name
        self.student_ids = student_ids

base_url = "https://api.vk.com/method"
token = os.environ['TOKEN']

def get_poll_answers(poll_id, owner_id):
    query = f"{base_url}/polls.getById?" \
            f"owner_id={owner_id}&" \
            f"poll_id={poll_id}&" \
            f"name_case=nom&v=5.131&" \
            f"access_token={token}"

    print(query)
    response_json = requests.get(query).json()
    answers_json = response_json["response"]["answers"]

    answers = {}
    for answer in answers_json:
        answers[answer['id']] = answer['text']
    lessons = get_vote_results(poll_id, answers)

    return lessons


def get_vote_results(poll_id, answers):
    answer_id_strs = ','.join(map(lambda key: str(key), answers.keys()))

    query = f"{base_url}/polls.getVoters?" \
            f"owner_id=736068632&" \
            f"poll_id={poll_id}&" \
            f"name_case=nom&v=5.131&" \
            f"answer_ids={answer_id_strs}&" \
            f"access_token={token}"

    response_json = requests.get(query).json()
    answers_json = response_json["response"]

    lessons = []
    for answer in answers_json:
        lesson = Lesson(answer['answer_id'], answers[answer['answer_id']], answer['users']['items'])
        lessons.append(lesson)
    return lessons

# gets from poll url owner and poll ids
def data_from_url():
    pass


app = FastAPI()
app.mount('/static',
          StaticFiles(directory='../front/build/static', html=True), name='static')

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def main():
    config = uvicorn.Config("main:app", port=7139, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

templates = Jinja2Templates(directory="../front/build")
@app.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/lessons")
async def get_lessons(owner_id, poll_id):
    return get_poll_answers(owner_id, poll_id)

@app.get("/students")
async def get_students():
    return get_students_from_file()

