from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    
    # Define a relationship to performance records (one-to-many)
    performance_records = relationship('PerformanceRecord', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    # Define a relationship to performance records (one-to-many)
    performance_records = relationship('PerformanceRecord', back_populates='course')

class PerformanceRecord(Base):
    __tablename__ = 'performance_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String(2))  # Assuming grades as strings like 'A', 'B', 'C'

    # Define relationships to students and courses (many-to-one)
    student = relationship('Student', back_populates='performance_records')
    course = relationship('Course', back_populates='performance_records')
