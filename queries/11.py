from sqlalchemy import func
from conf.db import DBSession
from conf.models import Student, Subject, Teacher, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2))\
                       .select_from(Student)\
                       .join(Grade)\
                       .join(Subject)\
                       .join(Teacher)\
                       .where(Student.id == 2)\
                       .where(Teacher.id == 2)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Student', 'Teacher', 'Subject']))
