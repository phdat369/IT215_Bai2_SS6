from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., gt=0)


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    for s in students:
        if s["code"] == student.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code already exists"
            )

    new_student = {
        "id": len(students) + 1,
        **student.model_dump()
    }

    students.append(new_student)

    return {
        "message": "Student created successfully",
        "data": new_student
    }

@app.get("/students")
def get_students(
    keyword: str | None = Query(None),
    min_age: int | None = Query(None, gt=0),
    max_age: int | None = Query(None, gt=0)
):
    result = students

    if keyword:
        keyword = keyword.lower()
        result = [
            s for s in result
            if keyword in s["name"].lower()
            or keyword in s["code"].lower()
            or keyword in s["email"].lower()
        ]

    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]

    return result


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must be greater than 0"
        )

    for s in students:
        if s["id"] == student_id:
            return s

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must be greater than 0"
        )

    for s in students:
        if s["code"] == student.code and s["id"] != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code already exists"
            )

    for index, s in enumerate(students):
        if s["id"] == student_id:
            students[index] = {
                "id": student_id,
                **student.model_dump()
            }

            return {
                "message": "Student updated successfully",
                "data": students[index]
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must be greater than 0"
        )

    for index, s in enumerate(students):
        if s["id"] == student_id:
            students.pop(index)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )