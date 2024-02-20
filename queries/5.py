from tabulate import tabulate
from conf.db import DBSession
from conf.models import Subject, Teacher


with DBSession() as session:
    qr = session.query(Teacher.fullname, Subject.name)\
                       .select_from(Subject)\
                       .join(Teacher)\
                       .where(Teacher.id == 2)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Teacher', 'Subject']))
