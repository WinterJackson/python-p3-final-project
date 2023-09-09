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

        expected_output = (
            f"Student Information:\n"
            f"Name: {student_name}\n"
            f"Student ID: {student_id}\n"
            f"Email: {student_email}\n"
            f"Age: {age}\n"
        )

        self.assertEqual(output, expected_output)

        # Test for a non-existent student
        non_existent_student_id = 999
        non_existent_output = self.sms.get_student_info(non_existent_student_id)

        expected_non_existent_output = f"Student with ID {non_existent_student_id} not found."
        self.assertEqual(non_existent_output, expected_non_existent_output)


    def test_get_course_info(self):
        # Add a course to the database using the StudentManagementSystem
        course_name = "Math 101"
        course_code = "MATH101"
        instructor = "Dr. Smith"
        start_date = "2023-09-01"
        end_date = "2023-12-15"
        self.sms.add_course(course_name, course_code, instructor, start_date, end_date)

        # Call get_course_info to retrieve the course information
        result = self.sms.get_course_info(course_code)

        # Define the expected output
        expected_output = (
            f"Course Name: {course_name}\n"
            f"Course Code: {course_code}\n"
            f"Instructor: {instructor}\n"
            f"Start Date: {start_date}\n"
            f"End Date: {end_date}\n"
        )

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)

    def test_get_performance_records(self):
        course_code = "MATH101"  

        # Call the get_performance_records method
        result = self.sms.get_performance_records(course_code)

        # Check if the course is not found
        if isinstance(result, str):
            self.assertEqual(result, f"Course with code {course_code} is not found.")
        else:
            # Check if the result is a list of dictionaries
            self.assertIsInstance(result, list)

            # Check the content of the result (example: checking the first record)
            self.assertTrue(len(result) > 0)  
            self.assertIn("student_id", result[0])
            self.assertIn("student_name", result[0])
            self.assertIn("attendance", result[0])
            self.assertIn("grade", result[0])


    def test_rank_students_valid_course_code(self):
        # Add a course and performance records for students
        course_code = "MATH101"
        self.sms.add_course("Math 101", course_code, "Dr. Smith", "2023-09-01", "2023-12-15")

        student_name_1 = "John Doe"
        self.sms.add_student(student_name_1, "john@example.com", 25)
        self.sms.add_performance_record(1, course_code, "B")

        student_name_2 = "Jane Smith"
        self.sms.add_student(student_name_2, "jane@example.com", 22)
        self.sms.add_performance_record(2, course_code, "A")

        student_name_3 = "Bob Johnson"
        self.sms.add_student(student_name_3, "bob@example.com", 24)
        self.sms.add_performance_record(3, course_code, "C")

        # Test ranking with a valid course code
        output = self.sms.rank_students(course_code)

        # Define the expected ranking based on grades
        expected_ranking = [
            (student_name_2, "A"),
            (student_name_1, "B"),
            (student_name_3, "C")
        ]

        # Extract the student names and grades from the output
        student_info = [(line[0], line[1]) for line in output]

        # Sort both the expected ranking and the actual ranking
        expected_ranking.sort(key=lambda x: x[0])  # Sort by student name
        student_info.sort(key=lambda x: x[0])  # Sort by student name

        # Compare the sorted expected ranking with the sorted actual ranking in the output
        for i, (expected_name, expected_grade) in enumerate(expected_ranking):
            self.assertEqual(student_info[i][0], expected_name)  # Check the student name
            self.assertEqual(student_info[i][1], expected_grade)  # Check the grade


    def test_rank_students_invalid_course_code(self):
        # Test ranking with an invalid course code
        invalid_course_code = "INVALIDCODE"
        output = self.sms.rank_students(invalid_course_code)

        # Define the expected error message
        expected_error_message = f"Course with code {invalid_course_code} is not found."

        # Check that the output matches the expected error message
        self.assertEqual(output, expected_error_message)



if __name__ == '__main__':
    unittest.main()
