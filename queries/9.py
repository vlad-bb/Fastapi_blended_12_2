from conf.db import DBSession
from conf.models import Student, Subject, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Student.fullname, Subject.name)\
                       .select_from(Student)\
                       .join(Grade)\
                       .join(Subject)\
                       .where(Student.id == 2)\
                       .group_by(Subject.name)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Student', 'Subject']))
