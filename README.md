# Database Schema

## Data to Be Stored

Students Table: This table will store information about each student, such as their name, student ID, email, and other relevant details.

Courses Table: This table will contain information about the courses available, including the course name, course code, and other course-related details.

Performance Records Table: This table will store performance data for each student in each course. It may include attributes like the student's ID, course code, grades, and any additional performance-related information.

## Schema

### Students Table:

Create a table named students.
Defines student attributes, such as:
id (Primary Key): A unique identifier for each student.
name: The name of the student.
email: The email address of the student.
age: The student's age.

### Courses Table:

Defines course attributes, such as:
course_code (Primary Key): A unique code for each course.
course_name: The name of the course.
instructor: The instructor or professor for the course.
start_date: The start date of the course.
end_date: The end date of the course.

### Performance Records Table:

Defines performance-related attributes, such as:
id (Primary Key): A unique identifier for each performance record.
student_id (Foreign Key): A reference to the student who earned the performance record.
student_name: The name of the student.
course_code (Foreign Key): A reference to the course for which the performance record is recorded.
grade: The grade or score achieved by the student in the course.
attendance: The average student attendance.