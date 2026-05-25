import importlib
import json

from fastapi.testclient import TestClient


def test_get_courses_returns_courses_from_json_file(tmp_path, monkeypatch):
    courses_file = tmp_path / "courses.json"
    expected_courses = [
        {
            "course_name": "자료구조",
            "year": "2025",
            "semester": "2",
            "grade": "A+",
        }
    ]
    courses_file.write_text(json.dumps(expected_courses, ensure_ascii=False), encoding="utf-8")

    main = importlib.import_module("main")
    monkeypatch.setattr(main, "COURSES_FILE", courses_file)
    client = TestClient(main.app)

    response = client.get("/courses")

    assert response.status_code == 200
    assert response.json() == expected_courses


def test_post_courses_adds_course_and_persists_to_json_file(tmp_path, monkeypatch):
    courses_file = tmp_path / "courses.json"
    courses_file.write_text("[]", encoding="utf-8")
    new_course = {
        "course_name": "인간로봇상호작용",
        "year": "2026",
        "semester": "2",
        "grade": "A+",
    }

    main = importlib.import_module("main")
    monkeypatch.setattr(main, "COURSES_FILE", courses_file)
    client = TestClient(main.app)

    response = client.post("/courses", json=new_course)

    assert response.status_code == 200
    assert response.json() == new_course
    assert json.loads(courses_file.read_text(encoding="utf-8")) == [new_course]


def test_invalid_post_request_does_not_stop_server(tmp_path, monkeypatch):
    courses_file = tmp_path / "courses.json"
    courses_file.write_text("[]", encoding="utf-8")

    main = importlib.import_module("main")
    monkeypatch.setattr(main, "COURSES_FILE", courses_file)
    client = TestClient(main.app)

    invalid_response = client.post("/courses", json={"course_name": "필드부족"})
    get_response = client.get("/courses")

    assert invalid_response.status_code == 422
    assert get_response.status_code == 200
    assert get_response.json() == []
