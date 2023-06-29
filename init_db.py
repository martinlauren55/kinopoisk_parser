from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
import json
params = json.load(open('params.json'))

engine = create_engine(f"sqlite:///pk_{params['start']}_{params['stop']}.db")  # for sqlite


class Base(DeclarativeBase):
    pass


class Film(Base):
    __tablename__ = 'Film'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kp_id = Column(Integer, nullable=False, comment='ID фильма')
    link = Column(String, nullable=False, comment='Полная ссылка')
    title = Column(String, nullable=False, comment='Название фильма')
    original_title = Column(String, nullable=False, comment='Оригинальное название')
    top_text = Column(String, nullable=False, comment='Текст дополнительный')
    poster = Column(String, nullable=False, comment='Ссылки на постер')
    production_year = Column(String, nullable=False, comment='Год производства')
    platform = Column(String, nullable=False, comment='Платформа')
    country = Column(String, nullable=False, comment='Страна')
    genre = Column(String, nullable=False, comment='Жанр')
    tagline = Column(String, nullable=False, comment='Слоган')
    director = Column(String, nullable=False, comment='Режиссер')
    scenario = Column(String, nullable=False, comment='Сценарий')
    producer = Column(String, nullable=False, comment='Продюсер')
    operator = Column(String, nullable=False, comment='Оператор')
    composer = Column(String, nullable=False, comment='Композитор')
    designer = Column(String, nullable=False, comment='Художник')
    edit = Column(String, nullable=False, comment='Монтаж')
    budget = Column(String, nullable=False, comment='Бюджет')
    marketing = Column(String, nullable=False, comment='Маркетинг')
    US_fees = Column(String, nullable=False, comment='Сборы в США')
    fees_in_the_world = Column(String, nullable=False, comment='Сборы в мире')
    fees_in_Russia = Column(String, nullable=False, comment='Сборы в России')
    premiere_in_Russia = Column(String, nullable=False, comment='Премьера в Росcии')
    world_Premiere = Column(String, nullable=False, comment='Премьера в мире')
    age = Column(String, nullable=False, comment='Возрастное ограничение')
    MPAA_rating = Column(String, nullable=False, comment='Рейтинг MPAA')
    time = Column(String, nullable=False, comment='Время')
    cast_list = Column(String, nullable=False, comment='Актеры')
    film_sinopsis = Column(String, nullable=False, comment='Описание фильма')
    rating = Column(String, nullable=False, comment='Рейтинг фильма')
    count_estimate = Column(String, nullable=False, comment='Кол-во оценок')



Base.metadata.create_all(engine)
