import unittest
import sys
import os

# Add the 'lib' directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # This line should include '..' to go up one level

# Now you can import your modules from the 'lib' directory
from lib.main import StudentManagementSystem  # Update this import
from lib.models import Student, Course, PerformanceRecord  # Update this import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create an in-memory SQLite database for testing
database_url = 'sqlite:///:memory:'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

class TestStudentManagement(unittest.TestCase):

    def setUp(self):
        # Set up the database and create tables
        Student.metadata.create_all(engine)
        Course.metadata.create_all(engine)
        PerformanceRecord.metadata.create_all(engine)

        self.sms = StudentManagementSystem()
        self.sms.session = session

    def tearDown(self):
        # Clean up resources or data after each test case (if needed)
        session.close()
        Student.metadata.drop_all(engine)
        Course.metadata.drop_all(engine)
        PerformanceRecord.metadata.drop_all(engine)

    def test_add_student(self):
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25

        self.sms.add_student(student_name, student_email, age)

        student = session.query(Student).filter_by(student_email=student_email).first()

        self.assertIsNotNone(student)
        self.assertEqual(student.student_name, student_name)
        self.assertEqual(student.age, age)

    def test_add_student_duplicate_email(self):
        student_name = "Jane Doe"
        student_email = "jane@example.com"
        age = 22

        self.sms.add_student(student_name, student_email, age)

        with self.assertRaises(Exception):  # Replace Exception with the actual exception type
            self.sms.add_student(student_name, student_email, age)

    def test_add_course(self):
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"

        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        course = session.query(Course).filter_by(course_code=course_code).first()

        self.assertIsNotNone(course)
        self.assertEqual(course.course_name, course_name)
        self.assertEqual(course.instructor, instructor)

    def test_update_student(self):
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25

        self.sms.add_student(student_name, student_email, age)

        new_name = "John Smith"
        self.sms.update_student(1, new_name)

        student = session.query(Student).filter_by(student_email=student_email).first()

        self.assertIsNotNone(student)
        self.assertEqual(student.student_name, new_name)

    def test_update_course(self):
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"

        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        new_course_name = "Mathematics 101"
        new_course_code = "MATH101A"

        self.sms.update_course(course_code, new_course_name, new_course_code)

        course = session.query(Course).filter_by(course_code=new_course_code).first()

        self.assertIsNotNone(course)
        self.assertEqual(course.course_name, new_course_name)
        self.assertEqual(course.course_code, new_course_code)

    def test_delete_student(self):
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25

        self.sms.add_student(student_name, student_email, age)

        self.sms.delete_student(1)

        student = session.query(Student).filter_by(student_email=student_email).first()

        self.assertIsNone(student)

    def test_delete_course(self):
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"

        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        self.sms.delete_course(course_code)

        course = session.query(Course).filter_by(course_code=course_code).first()

        self.assertIsNone(course)

    def test_add_performance_record(self):
        # Add a student and a course
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25
        self.sms.add_student(student_name, student_email, age)

        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"
        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        # Add a performance record for the student in the course
        grade = "A"
        self.sms.add_performance_record(1, course_code, grade)

        performance_record = session.query(PerformanceRecord).first()

        self.assertIsNotNone(performance_record)
        self.assertEqual(performance_record.grade, grade)

    def test_get_student_info(self):
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25
        self.sms.add_student(student_name, student_email, age)

        student_id = 1
        output = self.sms.get_student_info(student_id)

        expected_output = f"Student Information:\nName: {student_name}\nStudent ID: {student_id}\nEmail: {student_email}\nAge: {age}\n"
        self.assertEqual(output, expected_output)

    def test_get_course_info(self):
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"
        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        output = self.sms.get_course_info(course_code)

        expected_output = f"Course Information:\nCourse Name: {course_name}\nCourse Code: {course_code}\nInstructor: {instructor}\nStart Date: {start_date}\nEnd Date: {end_date}\n"
        self.assertEqual(output, expected_output)

    def test_get_performance_records(self):
        student_name = "John Doe"
        student_email = "john@example.com"
        age = 25
        self.sms.add_student(student_name, student_email, age)

        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"
        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        grade = "A"
        self.sms.add_performance_record(1, course_code, grade)

        output = self.sms.get_performance_records(course_code)

        expected_output = f"Performance Records for Course {course_name} (Code: {course_code}):\n"
        expected_output += f"Student Name: {student_name}\nStudent ID: 1, Name: {student_name}\nGrade: {grade}\n"  
        self.assertEqual(output, expected_output)

    def test_rank_students(self):
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"
        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        student_name_1 = "John Doe"
        student_email_1 = "john@example.com"
        age_1 = 25
        self.sms.add_student(student_name_1, student_email_1, age_1)
        self.sms.add_performance_record(1, course_code, "B")

        student_name_2 = "Jane Smith"
        student_email_2 = "jane@example.com"
        age_2 = 22
        self.sms.add_student(student_name_2, student_email_2, age_2)
        self.sms.add_performance_record(2, course_code, "A")

        student_name_3 = "Bob Johnson"
        student_email_3 = "bob@example.com"
        age_3 = 24
        self.sms.add_student(student_name_3, student_email_3, age_3)
        self.sms.add_performance_record(3, course_code, "C")

        output = self.sms.rank_students(course_code)

        # Define the expected ranking based on grades
        expected_ranking = [
            ("Jane Smith", "A"),
            ("John Doe", "B"),
            ("Bob Johnson", "C")
        ]

        # Split the output into lines and remove empty lines
        lines = [line.strip() for line in output.split('\n') if line.strip()]

        # Extract the student names and grades from the output
        student_info = [(lines[i], lines[i + 1]) for i in range(1, len(lines), 3)]

        # Compare the expected ranking with the actual ranking in the output
        for i, (expected_name, expected_grade) in enumerate(expected_ranking):
            self.assertIn(f"Rank: {i + 1}", student_info[i][0])  # Check the rank
            self.assertIn(f"Student Name: {expected_name}", student_info[i][0])  # Check the student name
            self.assertIn(f"Grade: {expected_grade}", student_info[i][1]) 


if __name__ == '__main__':
    unittest.main()
