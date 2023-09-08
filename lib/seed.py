from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Course, PerformanceRecord  # Adjust the import path as needed
from datetime import datetime


def populate_mock_data():
    # Define the database URL (same as in main.py)
    database_url = 'sqlite:///student_management.db'

    # Create the database engine
    engine = create_engine(database_url)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Populate the 'students' table with mock data
    students_data = [
        {'student_name': 'John Doe', 'student_email': 'john@example.com', 'age': 25},
        {'student_name': 'Jane Smith', 'student_email': 'jane@example.com', 'age': 24},
        {'student_name': 'Jojo Kantai', 'student_email': 'kantai@example.com', 'age': 20},
        {'student_name': 'Abdul Abdala', 'student_email': 'abdul@example.com', 'age': 21},
        {'student_name': 'Wendy Wafula', 'student_email': 'wendy@example.com', 'age': 21},
    ]

    for data in students_data:
        student = Student(**data)
        session.add(student)

    # Convert date strings to Python date objects
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    # Populate the 'courses' table with mock data
    courses_data = [
        {'course_name': 'Math 101', 'course_code': 'MATH101', 'instructor': 'Dr. Smith', 'start_date': '2023-09-01', 'end_date': '2023-12-15'},
        {'course_name': 'Physics 101', 'course_code': 'PHYS101', 'instructor': 'Prof. Johnson', 'start_date': '2023-09-01', 'end_date': '2023-12-15'},
        {'course_name': 'Chemistry 101', 'course_code': 'CHEM101', 'instructor': 'Prof. Johnson', 'start_date': '2023-09-01', 'end_date': '2023-12-15'},
        {'course_name': 'Biology 101', 'course_code': 'BIO101', 'instructor': 'Dr. Kamande', 'start_date': '2023-09-01', 'end_date': '2023-12-15'},
        {'course_name': 'English 101', 'course_code': 'ENG101', 'instructor': 'Prof. Rose', 'start_date': '2023-09-01', 'end_date': '2023-12-15'},
    ]

    for data in courses_data:
        data['start_date'] = parse_date(data['start_date'])
        data['end_date'] = parse_date(data['end_date'])
        course = Course(**data)
        session.add(course)

    # Populate the 'performance_records' table with mock data
    performance_records_data = [
        {'student_id': 1, 'course_id': 1, 'grade': 'A'},
        {'student_id': 2, 'course_id': 1, 'grade': 'B'},
        {'student_id': 3, 'course_id': 1, 'grade': 'C'},
        {'student_id': 4, 'course_id': 1, 'grade': 'B'},
        {'student_id': 5, 'course_id': 1, 'grade': 'D'},
    ]

    for data in performance_records_data:
        performance_record = PerformanceRecord(**data)
        session.add(performance_record)

    # Commit the changes to the database
    session.commit()

if __name__ == "__main__":
    populate_mock_data()
