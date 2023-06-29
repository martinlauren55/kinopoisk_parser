import ast

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_db import Film
from datetime import datetime
import json
params = json.load(open('params.json'))

class ManageDB:
    def __init__(self):
        self._dt_now = datetime.now()

        _engine = create_engine(f"sqlite:///pk_{params['start']}_{params['stop']}.db")  # for sqlite
        _session = sessionmaker(bind=_engine)
        self._s = _session()

    def ADD_FILM(self, kp_id, full_link, title, origin_title, top_text, poster, year, platform, country,
                 genre, tagline, director, scenario, producer, operator, composer, designer, edit, budget,
                 marketing, US_fees, fees_in_the_world, fees_in_Russia, premiere_in_Russia, world_Premiere,
                 age, MPAA_rating, time, cast_list, film_sinopsis, rating, count_estimate):

        f = Film(kp_id=kp_id, link=full_link, title=title, original_title=origin_title, top_text=top_text,
                 poster=str(poster), production_year=year, platform=platform, country=str(country), genre=str(genre),
                 tagline=tagline, director=str(director), scenario=str(scenario), producer=str(producer),
                 operator=str(operator), composer=str(composer), designer=str(designer), edit=str(edit), budget=str(budget),
                 marketing=str(marketing), US_fees=US_fees, fees_in_the_world=fees_in_the_world, fees_in_Russia=fees_in_Russia,
                 premiere_in_Russia=premiere_in_Russia, world_Premiere=world_Premiere, age=age, MPAA_rating=MPAA_rating,
                 time=time, cast_list=str(cast_list), film_sinopsis=film_sinopsis, rating=rating, count_estimate=count_estimate)

        self._s.add(f)
        self._s.commit()

    def _from_list_to_spisok(self, str_list):
        c_list = ast.literal_eval(str_list)
        result = ''
        for i, item in enumerate(c_list):
            if len(c_list) > 1:
                if i == 0:
                    result = item
                else:
                    result += ', ' + item
            else:
                result = item

        return result
