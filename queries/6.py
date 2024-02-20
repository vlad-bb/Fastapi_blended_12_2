from tabulate import tabulate
from conf.db import DBSession
from conf.models import Student, Group


with DBSession() as session:
    qr = session.query(Student.fullname, Group.name)\
                       .select_from(Student)\
                       .join(Group)\
                       .where(Group.id == 2)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Student', 'Group']))
