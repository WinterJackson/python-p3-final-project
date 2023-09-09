# Student Management System (SMS) CLI Application

The **Student Management System (SMS) CLI Application** is a Python command-line tool designed to help schools and educational institutions manage student data, courses, and performance records efficiently. This README provides an overview of the application's features, installation instructions, usage guide, and testing details.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Populating Mock Data](#populating-mock-data)
- [Running Tests](#running-tests)

---

## Features

The SMS CLI Application offers the following key features:

1. **Student Management:**
   - Add students with details such as name, email, and age.
   - Update student information, including their name.
   - Delete students from the database.

2. **Course Management:**
   - Add courses with details like course name, course code, instructor, start date, and end date.
   - Update course information, including course name and code.
   - Delete courses from the database.

3. **Performance Records:**
   - Add performance records for students in specific courses, including grades.
   - Retrieve performance records for courses and students.

4. **Data Retrieval:**
   - Retrieve detailed student information, including enrolled courses and grades.
   - Retrieve course information, including the course name, code, instructor, start date, and end date.

5. **Ranking Students:**
   - Rank students based on their grades in a specific course.

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10 installed on your system.
- `pipenv` installed. If not, you can install it using `pip`:

pip install pipenv

## Installation

To set up the SMS CLI Application, follow these steps:

1. **Clone the Repository:**

git clone <repository-url>
cd student-management-system-cli

2. **Create a Virtual Environment:**

pipenv install --python 3.10

3. **Activate the Virtual Environment:**

pipenv shell

4. **Install Dependencies:**

pipenv install

5. **Initialize the Database:**

python main.py or python3 main.py

## Usage

To interact with the SMS CLI Application, use the following commands:

- **Adding a Student:**

python main.py add_student <name> <email> <age>

- **Adding a Course:**

python main.py add_course <course_name> <course_code> <instructor> <start_date> <end_date>

- **Adding a Performance Record:**

python main.py add_performance_record <student_id> <course_code> <grade>

- **Updating Student Information:**

python main.py update_student <student_id> <new_name>

- **Updating Course Information:**

python main.py update_course <course_code> <new_course_name> <new_course_code>

- **Deleting a Student:**

python main.py delete_student <student_id>

- **Deleting a Course:**

python main.py delete_course <course_code>

- **Getting Student Information:**

python main.py get_student_info <student_id>

- **Getting Course Information:**

python main.py get_course_info <course_code>

- **Ranking Students:**

python main.py rank_students <course_code>

## Populating Mock Data

To populate the database with initial mock data for testing and development, use the provided `seed.py` script:

1. **Run the Script:**

python seed.py

2. The script will populate the database with sample student, course, and performance record data.

3. Customize the mock data by modifying the dictionaries within the `seed.py` script.

4. To start with an empty database, delete the `student_management.db` file and rerun the `seed.py` script.

## Running Tests

To ensure the functionality and correctness of the SMS CLI Application, run the unit tests provided in the `test_student_management.py` file:

1. **Run Tests:**

python -m unittest test_student_management.py

The Student Management System (SMS) CLI Application simplifies student data management for educational institutions. It offers a user-friendly interface for adding, updating, and retrieving student and course information, making it a valuable tool for efficient school administration.

*Developed by John Winter.*
*Contact winterjacksonwj@gmail.com.*

Enjoy using the SMS CLI Application!
