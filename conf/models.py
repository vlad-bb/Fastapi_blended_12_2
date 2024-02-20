from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, declarative_base, mapped_column, Mapped
from conf.db import DBSession, engine
from datetime import date

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    group: Mapped[Group] = relationship()


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    teacher: Mapped[Teacher] = relationship()


class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    grade_date: Mapped[date] = mapped_column(nullable=False)
    student: Mapped[Student] = relationship()
    subject: Mapped[Subject] = relationship()


def main():
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    with DBSession() as session:
        new_student = Student(fullname='Bill', group_id=1)
        session.add(new_student)
        session.commit()

        for student in session.query(Student).all():
            print(student.fullname, student.group_id)
            # session.delete(student)
            # session.commit()
        for group in session.query(Group).all():
            print(group.name, group.id, group)


def drop_db():
    with DBSession() as session:
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Grade).delete()
        session.query(Teacher).delete()
        session.query(Subject).delete()
        session.commit()


def show_db():
    with DBSession() as session:
        print('Persons------------------>')
        for student in session.query(Student).all():
            print(student.fullname)
        print('Teachers------------------>')
        for teacher in session.query(Teacher).all():
            print(teacher.fullname)
        print('Grades------------------>')
        for grade in session.query(Grade).all():
            print(grade.grade)
        print('Groups------------------>')
        for group in session.query(Group).all():
            print(group.name)
        print('Subjects------------------>')
        for subject in session.query(Subject).all():
            print(subject.name)


if __name__ == '__main__':
    # main()
    # drop_db()
    show_db()
