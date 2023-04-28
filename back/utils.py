import json


def get_students_from_file():
    file = open("students.json", 'r', encoding='utf-8')
    students = json.loads(file.read())
    file.close()
    return students