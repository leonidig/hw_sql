from datetime import datetime
from sqlalchemy import create_engine, String, select, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker


engine = create_engine("sqlite:///my.sql", echo=True)


class Base(DeclarativeBase):
    unit_id: Mapped[int] = mapped_column(primary_key=True)


#OUR MODELS



class Event(Base):
    __tablename__ = "chek_events"
    name: Mapped[str] = mapped_column(String(30))
    start: Mapped[datetime] 
    end: Mapped[datetime]
    status: Mapped[bool]



Base.metadata.create_all(engine)
Session = sessionmaker(engine)

name = input("Enter Name: ")
start = datetime.strptime(input("Enter start time: "), "%Y-%m-%d")
end = datetime.strptime(input("Enter end  time: "), "%Y-%m-%d")
status = input("Enter status (do / not): ")
if status == "do":
    status = True
else:
    status = False


filter_s = datetime.strptime(input("Enter a start date filter: "), "%Y-%m-%d")
filter_e = datetime.strptime(input("Enter a and date filter: "), "%Y-%m-%d")


with Session.begin() as session:
    event = Event(name=name, start=start, end=end, status=status)
    session.add(event)
    events = session.scalars(select(Event).where(Event.start >= filter_s).where(Event.end <= filter_e)).all()
    done = 0
    not_done = 0
    total_e = len(events)
    for item in events:
        if item.status == True:
            done += 1
        else:
            not_done += 1
        
    rate = (done / total_e) * 100
    print(f'Total events = {total_e}\nDone = {done}\nNot done = {not_done}\nRate = {rate}')




