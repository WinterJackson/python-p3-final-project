from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Define a relationship to performance records (one-to-many)
    performance_records = relationship('PerformanceRecord', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(255), unique=True, nullable=False)  
    course_name = Column(String(255), nullable=False)
    instructor = Column(String(255))  
    start_date = Column(Date)  
    end_date = Column(Date)
    
    # Define a relationship to performance records (one-to-many)
    performance_records = relationship('PerformanceRecord', back_populates='course')

class PerformanceRecord(Base):
    __tablename__ = 'performance_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    num_days_present = Column(Integer)
    attendance = Column(Float)
    grade = Column(String(2))

    # Define relationships to students and courses (many-to-one)
    student = relationship('Student', back_populates='performance_records')
    course = relationship('Course', back_populates='performance_records')

    def calculate_attendance(self):
        if self.num_days_present is not None and self.course is not None:
            start_date = self.course.start_date
            end_date = self.course.end_date

            # Calculate the number of days between start_date and end_date (inclusive)
            total_days = (end_date - start_date).days + 1

            # Calculate attendance percentage
            if total_days > 0:
                self.attendance = (self.num_days_present / total_days) * 100
            else:
                self.attendance = 0  

    @property
    def num_days_present(self):
        return self._num_days_present

    @num_days_present.setter
    def num_days_present(self, value):
        self._num_days_present = value
        self.calculate_attendance()
