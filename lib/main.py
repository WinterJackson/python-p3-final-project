import fire
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Course, PerformanceRecord

database_url = 'sqlite:///student_management.db'
engine = create_engine(database_url)

# Create tables in the database based on the models
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class StudentManagementSystem:
    def __init__(self):
        self.session = session  

    def add_student(self, name, student_id, email, age):
        """Add a new student to the database."""
        # Create a new Student object and add it to the session
        new_student = Student(name=name, student_id=student_id, email=email, age=age)
        self.session.add(new_student)
        
        # Commit the changes to the database
        self.session.commit()
        print(f"Added student: {name} (ID: {student_id}, Email: {email}, Age: {age})")

    def add_course(self, course_name, course_code, instructor, start_date, end_date):
        """Add a new course to the database."""
        # Create a new Course object and add it to the session
        new_course = Course(
            course_name=course_name,
            course_code=course_code,
            instructor=instructor,
            start_date=start_date,
            end_date=end_date
        )
        self.session.add(new_course)
        
        # Commit the changes to the database
        self.session.commit()
        print(f"Added course: {course_name} (Code: {course_code}, Instructor: {instructor}, Start Date: {start_date}, End Date: {end_date}))")

    def add_performance_record(self, student_id, course_code, grade):
        """Add a performance record for a student in a course."""
        # Retrieve the student and course based on student_id and course_code
        student = self.session.query(Student).filter_by(student_id=student_id).first()
        course = self.session.query(Course).filter_by(course_code=course_code).first()
        
        if student is None:
            print(f"Student with ID {student_id} not found.")
            return
        
        if course is None:
            print(f"Course with code {course_code} not found.")
            return
        
        # Create a new PerformanceRecord object and add it to the session
        new_performance_record = PerformanceRecord(student=student, course=course, grade=grade)
        self.session.add(new_performance_record)
        
        # Commit the changes to the database
        self.session.commit()
        print(f"Added performance record: Student ID: {student_id}, Course Code: {course_code}, Grade: {grade}")

    def get_student_info(self, student_id):
        """Retrieve and display detailed student information."""
        # Retrieve the student based on student_id
        student = self.session.query(Student).filter_by(student_id=student_id).first()

        if student is None:
            print(f"Student with ID {student_id} not found.")
            return

        print(f"Student Information:\nName: {student.name}\nStudent ID: {student.student_id}\nEmail: {student.email}\nAge: {student.age}\n")

        # Retrieve the performance records for the student, including course information
        performance_records = self.session.query(PerformanceRecord).filter_by(student_id=student_id).all()

        if not performance_records:
            print("No performance records found for this student.")
        else:
            print("Courses and Grades:")
            for record in performance_records:
                course = record.course
                print(f"Course: {course.course_name} (Code: {course.course_code})")
                print(f"Grade: {record.grade}")
                print(f"Attendance: {record.attendance}")  
                print("-" * 40)  # Separator between courses

    def get_course_info(self, course_code):
        """Retrieve and display course information, including enrolled students."""
        # Retrieve the course based on course_code
        course = self.session.query(Course).filter_by(course_code=course_code).first()

        if course is None:
            print(f"Course with code {course_code} is not found.")
            return

        print(f"Course Information:\nCourse Name: {course.course_name}\nCourse Code: {course.course_code}\nInstructor: {course.instructor}\nStart Date: {course.start_date}\nEnd Date: {course.end_date}\n")

        # Retrieve the students enrolled in this course
        enrolled_students = [record.student for record in course.performance_records]

        if not enrolled_students:
            print("No students enrolled in this course.")
        else:
            print("Enrolled Students:")
            for student in enrolled_students:
                print(f"Student ID: {student.student_id}, Name: {student.name}")

    def get_performance_records(self, course_code):
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
                print(f"Student Name: {student.name}")
                print(f"Student ID: {student.student_id}, Name: {student.name}")

                # Check if attendance information is available for this record
                if hasattr(record, 'attendance'):
                    print(f"Attendance: {record.attendance}")
                    print(f"Number of Days Present: {record.num_days_present}")
                print(f"Grade: {record.grade}")
                print("-" * 40)  # Separator between students

if __name__ == "__main__":
    sms = StudentManagementSystem()
    fire.Fire(sms)

