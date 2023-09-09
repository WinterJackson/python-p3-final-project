
import fire
from datetime import datetime 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from .models import Base, Student, Course, PerformanceRecord, Enrollment

# Define the database URL
database_url = 'sqlite:///student_management.db'

# Create the database engine
engine = create_engine(database_url)

# Create tables in the database based on the models
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class StudentManagementSystem:
    def __init__(self):
        self.session = session

    def add_student(self, name: str, email: str, age: int):
        """Add a new student to the database."""
        new_student = Student(student_name=name, student_email=email, age=age)
        self.session.add(new_student)
        self.session.commit()
        print(f"Added student: {new_student.student_name} (ID: {new_student.id}, Email: {new_student.student_email}, Age: {age})")

    def add_course(self, course_name: str, course_code: str, instructor: str, start_date, end_date):
        """Add a new course to the database."""
        # Convert date strings to date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        new_course = Course(
            course_name=course_name,
            course_code=course_code,
            instructor=instructor,
            start_date=start_date,
            end_date=end_date
        )
        self.session.add(new_course)
        self.session.commit()
        print(f"Added course: {course_name} (Code: {course_code}, Instructor: {instructor}, Start Date: {start_date}, End Date: {end_date})")

    def add_performance_record(self, student_id, course_code, grade):
        """Add a performance record for a student in a course."""
        # Retrieve the student and course based on student_id and course_code
        student = self.session.query(Student).filter_by(id=student_id).first()
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if student is None:
            print(f"Student with ID {student_id} not found.")
            return

        if course is None:
            print(f"Course with code {course_code} not found.")
            return

        # Create a new PerformanceRecord object and add it to the session
        new_performance_record = PerformanceRecord(student_id=student_id, course_id=course.id, num_days_present=0, grade=grade)
        self.session.add(new_performance_record)

        # Commit the changes to the database
        self.session.commit()
        print(f"Added performance record: Student ID: {student_id}, Course Code: {course_code}, Grade: {grade}")

    def update_student(self, id, new_name: str):
        """Update student information."""
        student = self.session.query(Student).filter_by(id=id).first()

        if student is None:
            print(f"Student with ID {id} not found.")
            return

        student.student_name = new_name
        self.session.commit()
        print(f"Updated student information: Student ID: {id}, New Name: {new_name}")

    def update_course(self, course_code: str, new_course_name: str, new_course_code: str):
        """Update course information."""
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            print(f"Course with code {course_code} not found.")
            return

        course.course_name = new_course_name
        course.course_code = new_course_code
        self.session.commit()
        print(f"Updated course information: Course Code: {new_course_code}, New Course Name: {new_course_name}")

    def delete_student(self, id):
        """Delete a student."""
        student = self.session.query(Student).filter_by(id=id).first()

        if student is None:
            print(f"Student with ID {id} not found.")
            return

        self.session.delete(student)
        self.session.commit()
        print(f"Deleted student: Student ID: {id}")

    def delete_course(self, course_code: str):
        """Delete a course."""
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            print(f"Course with code {course_code} not found.")
            return

        self.session.delete(course)
        self.session.commit()
        print(f"Deleted course: Course Code: {course_code}")

    def get_student_info(self, student_id):
        # Query the database to get the student by ID
        student = self.session.query(Student).filter_by(id=student_id).first()

        if student is None:
            return f"Student with ID {student_id} not found."

        # Fetch the student's courses and grades using a join
        student_courses = (
            self.session.query(Course, PerformanceRecord)
            .filter(PerformanceRecord.student_id == student.id)
            .join(Course, Course.id == PerformanceRecord.course_id)
            .all()
        )

        # Format the result with student information
        student_info = (
            f"Student Information:\n"
            f"Name: {student.student_name}\n"
            f"Student ID: {student.id}\n"
            f"Email: {student.student_email}\n"
            f"Age: {student.age}\n"
        )

        # Check if the student has enrolled in any courses
        if student_courses:
            student_info += "Courses Enrolled:\n"
            for course, grade in student_courses:
                student_info += f"- {course.course_name} (Code: {course.course_code}), Grade: {grade.grade}\n"

        return student_info

    def get_course_info(self, course_code):
        """
        Get course information based on course code.
        
        Args:
            course_code (str): The code of the course to retrieve.
        
        Returns:
            str: A formatted string with course information.
        """
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            return f"Course with code {course_code} is not found."

        # Format and return course information
        course_info = (
            f"Course Name: {course.course_name}\n"
            f"Course Code: {course.course_code}\n"
            f"Instructor: {course.instructor}\n"
            f"Start Date: {course.start_date}\n"
            f"End Date: {course.end_date}\n"
        )
        return course_info

    def get_performance_records(self, course_code):
        # Query the course by its course_code
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if not course:
            return f"Course with code {course_code} is not found."

        # Query the performance records for the course, including student names and IDs
        records = self.session.query(PerformanceRecord, Student).\
            join(Student).filter(PerformanceRecord.course_id == course.id).all()

        # Prepare the results as a list of dictionaries
        performance_data = []
        for record, student in records:
            performance_data.append({
                "student_id": student.id,
                "student_name": student.student_name,
                "attendance": record.attendance,  
                "grade": record.grade
            })

        return performance_data

    def rank_students(self, course_code):
        """
        Rank students in descending order based on their grade in a specific course.
        Args:
            course_code (str): The course code for which to rank students.
        Returns:
            list or str: A list of tuples containing (student_name, grade) in descending order
                            or an error message if the course code is not found.
        """
        # Check if the course code exists in the database
        course = self.session.query(Course).filter_by(course_code=course_code).first()
        if not course:
            return f"Course with code {course_code} is not found."

        # Query the database to get the ranked students
        ranked_students = self.session.query(Student.student_name, PerformanceRecord.grade)\
            .join(PerformanceRecord, Student.id == PerformanceRecord.student_id)\
            .join(Course, PerformanceRecord.course_id == Course.id)\
            .filter(Course.course_code == course_code)\
            .order_by(desc(PerformanceRecord.grade))\
            .all()

        return ranked_students

if __name__ == "__main__":
    sms = StudentManagementSystem()
    fire.Fire(sms)
