import os
import requests as requests
from back.entities import Lesson

base_url = "https://api.vk.com/method"
token = os.environ['TOKEN']

def get_poll_answers(poll_id, owner_id):
    query = f"{base_url}/polls.getById?" \
            f"owner_id={owner_id}&" \
            f"poll_id={poll_id}&" \
            f"name_case=nom&v=5.131&" \
            f"access_token={token}"

    response_json = requests.get(query).json()
    answers_json = response_json["response"]["answers"]

    answers = dict()
    for answer in answers_json:
        answers[answer['id']] = answer['text']

    return answers


def get_poll_lessons(poll_id, owner_id, answers):
    answer_ids_str = ','.join(map(lambda key: str(key), answers.keys()))

    query = f"{base_url}/polls.getVoters?" \
            f"owner_id={owner_id}&" \
            f"poll_id={poll_id}&" \
            f"name_case=nom&v=5.131&" \
            f"answer_ids={answer_ids_str}&" \
            f"access_token={token}"

    response_json = requests.get(query).json()
    answers_json = response_json["response"]

    lessons = []
    for answer in answers_json:
        lesson = Lesson(answer['answer_id'], answers[answer['answer_id']], answer['users']['items'])
        lessons.append(lesson)
    return lessons
