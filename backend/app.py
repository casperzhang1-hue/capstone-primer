from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
    
    if not student_data or 'name' not in student_data or 'course' not in student_data:
        return jsonify({'error': 'Name and course are required'}), 404
    
    name = student_data.get('name')
    course = student_data.get('course')
    mark = student_data.get('mark')
    
    if not name or not course:
        return jsonify({'error': 'Name and course cannot be empty'}), 404
    
    try:
        student = db.insert_student(name, course, mark)
        return jsonify(student), 200
    except Exception:
        return jsonify({'error': 'Failed to create student'}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student_route(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    
    name = student_data.get('name')
    course = student_data.get('course')
    mark = student_data.get('mark')
    
    student = db.update_student(student_id, name, course, mark)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student_route(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    result = db.delete_student(student_id)
    
    if not result:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(result), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [s['mark'] for s in students if s['mark'] is not None]
    
    count = len(marks)
    if not marks:
        return jsonify({
            'count': count,
            'average': None,
            'min': None,
            'max': None
        }), 200
    
    average = sum(marks) / len(marks)
    min_mark = min(marks)
    max_mark = max(marks)
    
    return jsonify({
        'count': count,
        'average': average,
        'min': min_mark,
        'max': max_mark
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
