from sqlalchemy import func, desc
from conf.db import DBSession
from conf.models import Student, Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(Student.fullname,
                       func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                       .select_from(Grade)\
                       .join(Student)\
                       .group_by(Student.id)\
                       .order_by(desc('avg_grade'))\
                       .limit(5).all()

    print(tabulate(qr, tablefmt='github', headers=['Name', 'Grade']))
