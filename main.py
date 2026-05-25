import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
COURSES_FILE = Path("courses.json")


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def load_courses():
    if not COURSES_FILE.exists():
        save_courses([])
        return []

    try:
        with COURSES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="courses.json 파일 형식이 올바르지 않습니다.") from exc

    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="courses.json 파일은 JSON list 형태여야 합니다.")

    return data


def save_courses(courses):
    with COURSES_FILE.open("w", encoding="utf-8") as file:
        json.dump(courses, file, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    return load_courses()


@app.post("/courses")
def add_course(course: Course):
    courses = load_courses()
    new_course = course.model_dump()
    courses.append(new_course)
    save_courses(courses)
    return new_course
