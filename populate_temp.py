from src.setup_db.database import db
from src.setup_db.models.m_ambient_temperature_tbl import AmbientTemperatureModel
from random import randint


class PopulateTemp:
    def __init__(self):
        self.populate_temperature()

    def populate_temperature(self):
        random_temp_list = []
        counter = 1

        while counter <= 1000:
            rand_num = randint(1, 100)
            random_temp_list.append(AmbientTemperatureModel(temp=rand_num))
            counter += 1

        db.session.bulk_save_objects(random_temp_list)
        db.session.commit()
