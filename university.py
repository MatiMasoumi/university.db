import sqlite3
# Establish connection to the database
connection = sqlite3.connect("university.db")
cursor = connection.cursor()
# 1. Create tables
cursor.execute("""
 CREATE TABLE IF NOT EXISTS Students ( StudentID INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT,
  LastName TEXT, DateOfBirth DATE, Email TEXT ); """)
cursor.execute("""
 CREATE TABLE IF NOT EXISTS Courses ( CourseID INTEGER PRIMARY KEY AUTOINCREMENT, CourseName TEXT, Instructor TEXT );
  """)
cursor.execute("""
 CREATE TABLE IF NOT EXISTS Enrollments ( EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT, StudentID INTEGER,
  CourseID INTEGER, EnrollmentDate DATE, FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
   ON DELETE CASCADE, FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE );
    """)
print("Tables created successfully.")
# 2. Insert sample data 
# --Students
cursor.execute("INSERT INTO Students(FirstName, LastName, DateOfBirth, Email) VALUES ('Ali', 'Ahmadi', '2000-05-15', 'ali.ahmadi@example.com')")
cursor.execute("INSERT INTO Students (FirstName, LastName, DateOfBirth, Email) VALUES ('Sara', 'Karimi', '1999-11-20','sara.karimi@example.com')")
cursor.execute("INSERT INTO Students (FirstName, LastName, DateOfBirth, Email) VALUES ('Reza', 'Hosseini', '2001-02-10','reza.hosseini@example.com')")
# -- Courses
cursor.execute("INSERT INTO Courses (CourseName, Instructor) VALUES ('Introduction to Java', 'Dr. Naderi')")
cursor.execute("INSERT INTO Courses (CourseName, Instructor) VALUES ('Data Structures', 'Dr. Shariati')")
cursor.execute("INSERT INTO Courses (CourseName, Instructor) VALUES ('Database Systems', 'Dr. Kaviani')")
# -- Enrollments
cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (1, 1, '2024-01-10')")
cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (1, 2, '2024-01-15')")
cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (2, 1, '2024-01-12')")
cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, EnrollmentDate) VALUES (3, 3, '2024-01-14')")
connection.commit()
print("Sample data inserted successfully.")
# 3. Query to display the number of courses each student is enrolled in
print("\nStudent Enrollments:")
cursor.execute(""" SELECT Students.FirstName || ' ' || Students.LastName AS StudentName,
 COUNT(Enrollments.CourseID) AS CourseCount FROM Students LEFT JOIN Enrollments ON
  Students.StudentID = Enrollments.StudentID GROUP BY Students.StudentID """)
results = cursor.fetchall()
for row in results:
   print(f"Name: {row[0]}, Courses Enrolled: {row[1]}")
# 4. Delete students who are enrolled in less than 2 courses
cursor.execute(""" DELETE FROM Students WHERE StudentID IN ( SELECT StudentID FROM Enrollments GROUP BY StudentID HAVING COUNT(CourseID)
 < 2 ); """)
connection.commit()
print("\nStudents with less than 2 enrollments removed.")
# 5. Update course names containing "Java" to "Python"
cursor.execute(""" UPDATE Courses SET CourseName = REPLACE(CourseName, 'Java', 'Python') WHERE CourseName LIKE '%Java%' """)
connection.commit()
# Verify changes
print("\nUpdated Courses:")
cursor.execute("SELECT * FROM Courses")
courses = cursor.fetchall()
for course in courses:
   print(course)
# Close the connection
connection.close()