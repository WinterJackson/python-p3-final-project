from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    performance_records = relationship('PerformanceRecord', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(255), unique=True, nullable=False)
    course_name = Column(String(255), nullable=False)
    instructor = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)

    performance_records = relationship('PerformanceRecord', back_populates='course')

class PerformanceRecord(Base):
    __tablename__ = 'performance_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String(2))
    _num_days_present = Column(Integer, default=0)
    
    student = relationship('Student', back_populates='performance_records')
    course = relationship('Course', back_populates='performance_records')

    @hybrid_property
    def num_days_present(self):
        return self._num_days_present

    @num_days_present.setter
    def num_days_present(self, value):
        self._num_days_present = value

    @hybrid_property
    def attendance(self):
        # Calculate attendance based on the provided '_num_days_present' and the total days
        if self.course is not None:
            start_date = self.course.start_date
            end_date = self.course.end_date

            total_days = (end_date - start_date).days + 1

            if total_days > 0:
                return (self.num_days_present / total_days) * 100
            else:
                return 0
        else:
            # If 'course' is not set, attendance cannot be calculated, so return None
            return None