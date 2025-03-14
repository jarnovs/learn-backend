from aiohttp.web import Application, json_response, run_app, get
from sqlalchemy import select, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine("sqlite:///db.db")
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]


async def hello(request):
    data = []
    with Session() as session:
        users = session.scalars(select(User))
        for user in users:
            data.append({"id": user.id, "name": user.name}) 
    return json_response(data)


if __name__ == "__main__":
    app = Application()
    Base.metadata.create_all(engine)
    app.add_routes([get('/', hello)])
    run_app(app)
