import asyncio
import os

import uvicorn as uvicorn
from fastapi import FastAPI

import requests as requests



# def get_access_token(client_id: int) -> None:
#     assert isinstance(client_id, int), 'clinet_id must be positive integer'
#     assert client_id > 0, 'clinet_id must be positive integer'
#
#     url = f"""\
#     https://oauth.vk.com/authorize
#     ?client_id={client_id}
#     &display=page
#     &redirect_uri=https://oauth.vk.com/blank.hmtl
#     &scope=wall
#     &response_type=token
#     &v=5.131
#     """.replace(" ", "").format(client_id=client_id, scope='wall')
#     webbrowser.open_new_tab(url)


dict_names = {
    1234: "StudentName"
}

class Lesson:
    def __init__(self, name, student_ids):
        self.name = name
        self.students = [dict_names[st_id] for st_id in student_ids]
        self.students.sort()

    def __str__(self):
        string = '<br>' + '<br>'.join(self.students)
        return f"{self.name}: {string}<br>"


domain = "https://api.vk.com/method"
token = os.environ['TOKEN']

app = FastAPI()
async def main():
    config = uvicorn.Config("main:app", port=7139, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

def get_poll_answers(poll_id='837100981', owner_id='736068632'):
    query = f"{domain}/polls.getById?" \
            f"owner_id={owner_id}&" \
            f"poll_id={poll_id}&name_case=nom&v=5.131&" \
            f"access_token={token}"
    response_json = requests.get(query).json()
    answers_json = response_json["response"]["answers"]

    answers = {}
    for answer in answers_json:
        answers[answer['id']] = answer['text']
    lessons = get_vote_results(poll_id, answers)

    return lessons


def get_vote_results(poll_id, answers):
    answer_id_strs = ','.join(map(lambda el: str(el), answers.keys()))

    query = f"{domain}/polls.getVoters?" \
            f"owner_id=736068632&" \
            f"poll_id={poll_id}&name_case=nom&v=5.131&" \
            f"answer_ids={answer_id_strs}&" \
            f"access_token={token}"

    response_json = requests.get(query).json()
    answers_json = response_json["response"]

    lessons = {}
    for el in answers_json:
        lessons[el['answer_id']] = Lesson(
            answers[el['answer_id']],
            el['users']['items']
        )
    return lessons

# gets from poll url owner and poll ids
def data_from_url():
    pass


@app.get("/")
def read_root():
    return get_poll_answers()
