from sqlalchemy import func
from conf.db import DBSession
from conf.models import Grade
from tabulate import tabulate


with DBSession() as session:
    qr = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                       .select_from(Grade)\
                       .all()

    print(tabulate(qr, tablefmt='github', headers=['Avg Grade']))
