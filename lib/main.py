
import fire
from datetime import datetime 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Student, Course, PerformanceRecord

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

    def get_student_info(self, id):
        """Retrieve and return detailed student information as a string."""
        # Retrieve the student based on student_id
        student = self.session.query(Student).filter_by(id=id).first()

        if student is None:
            return f"Student with ID {id} not found."

        student_info = f"Student Information:\nName: {student.student_name}\nStudent ID: {student.id}\nEmail: {student.student_email}\nAge: {student.age}\n"

        # Retrieve the performance records for the student, including course information
        performance_records = self.session.query(PerformanceRecord).filter_by(student_id=id).all()

        if not performance_records:
            return "No performance records found for this student."
        else:
            student_info += "Courses and Grades:\n"
            for record in performance_records:
                course = record.course
                student_info += f"Course: {course.course_name} (Code: {course.course_code})\n"
                student_info += f"Grade: {record.grade}\n"
                student_info += f"Attendance: {record.attendance}\n"
                student_info += "-" * 40 + "\n"  # Separator between courses

        return student_info

    def get_course_info(self, course_code: str):
        """Retrieve and return course information, including enrolled students, as a string."""
        # Retrieve the course based on course_code
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            return f"Course with code {course_code} is not found."

        course_info = f"Course Information:\n"
        course_info += f"Course Name: {course.course_name}\n"
        course_info += f"Course Code: {course.course_code}\n"
        course_info += f"Instructor: {course.instructor}\n"
        course_info += f"Start Date: {course.start_date}\n"
        course_info += f"End Date: {course.end_date}\n"

        # Retrieve the students enrolled in this course
        enrolled_students = [record.student for record in course.performance_records]

        if not enrolled_students:
            course_info += "No students enrolled in this course."
        else:
            course_info += "Enrolled Students:\n"
            for student in enrolled_students:
                course_info += f"Student ID: {student.id}, Name: {student.student_name}\n"

        return course_info

    def get_performance_records(self, course_code: str):
        """Retrieve and display performance records, including attendance, for every student enrolled in the specified course_code."""
        # Retrieve the course based on course_code
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            print(f"Course with code {course_code} is not found.")
            return

        print(f"Performance Records for Course {course.course_name} (Code: {course.course_code}):\n")

        # Retrieve the performance records for all students in this course
        performance_records = course.performance_records

        if not performance_records:
            print("No performance records found for this course.")
        else:
            for record in performance_records:
                student = record.student
                print(f"Student Name: {student.student_name}")
                print(f"Student ID: {student.id}, Name: {student.student_name}")

                # Check if attendance information is available for this record
                if hasattr(record, 'attendance'):
                    print(f"Attendance: {record.attendance}")
                    print(f"Number of Days Present: {record.num_days_present}")
                print(f"Grade: {record.grade}")
                print("-" * 40)  # Separator between students

    def rank_students(self, course_code: str):
        """Return students' performance ranked by grades for a specific course as a string."""
        # Retrieve the course based on course_code
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            return f"Course with code {course_code} is not found."

        ranking_info = f"Ranking for Course {course.course_name} (Code: {course.course_code}):\n"

        # Retrieve the performance records for all students in this course
        performance_records = course.performance_records

        if not performance_records:
            return "No performance records found for this course."

        # Sort students by grades in descending order
        sorted_records = sorted(performance_records, key=lambda record: record.grade, reverse=True)

        for rank, record in enumerate(sorted_records, start=1):
            student = record.student
            ranking_info += f"Rank: {rank}\n"
            ranking_info += f"Student Name: {student.student_name}\n"
            ranking_info += f"Grade: {record.grade}\n"
            ranking_info += "-" * 40 + "\n"

        return ranking_info


if __name__ == "__main__":
    sms = StudentManagementSystem()
    # sms.add_student("Abdul Abdala", "abdulabdala@example.com", 18)
    # sms.add_student("Keith Kimani", "keithkimani@example.com", 19)
    # sms.add_student("Brian Wetu", "brianwetu@example.com", 20)
    # sms.add_student("Wendy Wafula", "wendywafula@example.com", 21)
    # sms.add_student("Jojo Kantai", "jojokantai@example.com", 22)

    fire.Fire(sms)
