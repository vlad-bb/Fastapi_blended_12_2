from conf.db import DBSession
from conf.models import Student, Subject, Teacher, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Student.fullname, Teacher.fullname, Subject.name)\
                       .select_from(Student)\
                       .join(Grade)\
                       .join(Subject)\
                       .join(Teacher)\
                       .where(Student.id == 2)\
                       .where(Teacher.id == 2)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Student', 'Teacher', 'Subject']))
