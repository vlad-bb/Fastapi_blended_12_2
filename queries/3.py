from sqlalchemy import func, desc
from conf.db import DBSession
from conf.models import Student, Subject, Group, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Group.name, Subject.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                       .select_from(Group)\
                       .join(Student)\
                       .join(Grade)\
                       .join(Subject)\
                       .where(Subject.id == 1)\
                       .group_by(Group.name)\
                       .order_by(desc('avg_grade'))\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Group', 'Subject', 'Avg Grade']))
