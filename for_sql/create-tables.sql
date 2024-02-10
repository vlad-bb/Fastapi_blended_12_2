-- Таблиця груп
drop table if exists groups;
CREATE TABLE groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL
);

-- Таблиця студентів
drop table if exists students;
CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname VARCHAR(150) NOT NULL,
  group_id REFERENCES groups(id)
  	on delete cascade
);

-- Таблиця викладачів
drop table if exists teachers;
CREATE TABLE teachers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname VARCHAR(150) NOT NULL
);

-- Таблиця предметів
drop table if exists subjects;
CREATE TABLE subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(175) NOT NULL,
  teacher_id REFERENCES teachers(id)
  	on delete cascade
);

-- Таблиця оцінок
drop table if exists grades;
CREATE TABLE grades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id REFERENCES students(id)
  on delete cascade,
  subject_id REFERENCES subjects(id)
  on delete cascade,
  grade INTEGER CHECK (grade >= 0 AND grade <= 100),
  grade_date DATE NOT NULL
);