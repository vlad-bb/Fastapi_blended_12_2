from conf.db import DBSession
from conf.models import Student, Subject, Group, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Student.fullname, Subject.name, Grade.grade, Group.name)\
                       .select_from(Group)\
                       .join(Student)\
                       .join(Grade)\
                       .join(Subject)\
                       .where(Subject.id == 2)\
                       .where(Group.id == 2)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Student', 'Subject', 'Grade', 'Group']))
