from faker import Faker
from conf.models import Teacher, Group, Student, Subject, Grade
from conf.db import DBSession, engine
from conf.models import Base
from datetime import datetime, timedelta
from random import randint

fake = Faker()

Base.metadata.create_all(engine)
Base.metadata.bind = engine
with DBSession() as session:
    # Генерація груп
    groups = [Group(name=f'Group {i}') for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    # Генерація викладачів
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    # Генерація предметів
    subjects = [Subject(name=fake.word(), teacher_id=fake.random_element(teachers).id) for _ in range(8)]
    session.add_all(subjects)
    session.commit()

    # Генерація студентів та їх оцінок
    for _ in range(30):
        student = Student(fullname=fake.name(), group_id=fake.random_element(groups).id)
        session.add(student)
        session.commit()
        for subject in subjects:
            # Генеруємо випадкову дату в межах останніх 300 днів
            grade_date = datetime.now() - timedelta(days=randint(1, 300))
            grade = Grade(grade=fake.random_int(min=60, max=100), student_id=student.id, subject_id=subject.id,
                          grade_date=grade_date.date())
            session.add(grade)
        session.commit()
