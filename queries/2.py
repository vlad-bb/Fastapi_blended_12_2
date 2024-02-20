from sqlalchemy import func, desc
from conf.db import DBSession
from conf.models import Student, Subject, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Student.fullname, Subject.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                       .select_from(Grade)\
                       .join(Subject)\
                       .join(Student)\
                       .where(Subject.id == 1)\
                       .order_by(desc('avg_grade'))\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Name', 'Subject', 'Grade']))
