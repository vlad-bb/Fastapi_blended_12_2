from sqlalchemy import func
from conf.db import DBSession
from conf.models import Subject, Teacher, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                       .select_from(Teacher)\
                       .join(Subject)\
                       .join(Grade)\
                       .where(Teacher.id == 2)\
                       .group_by(Subject.name)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Teacher', 'Subject', 'Grade']))
