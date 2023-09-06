from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer)
    
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
    student_name = Column(String(255))  
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String(2))  
    attendance = Column(Float) 

    # Define relationships to students and courses (many-to-one)
    student = relationship('Student', back_populates='performance_records')
    course = relationship('Course', back_populates='performance_records')
