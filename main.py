import pickle
import random
from time import sleep
from loguru import logger
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from db_manager import ManageDB
import requests

browser = webdriver.Firefox()
DOMAIN = 'https://www.kinopoisk.ru/'

# pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
browser.get(DOMAIN)

sleep(5)
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

browser.refresh()

sleep(1)
params = json.load(open('params.json'))

logger.add(f"logs_{params['start']}_{params['stop']}.log", format="{time:YYYY-M-D HH:mm:ss} - {level} - {message}",
           level="DEBUG", rotation="13 MB", compression="zip")


class Get_Info_Film():
    def __init__(self, browser, link, id):
        self._db = ManageDB()
        self._browser = browser
        self._browser.get(link)
        self._link = link
        self._id = id
        self._TITLE = ''  # Название
        self._ORIGINAL_TITLE = ''  # Название на английском
        self._TOP_TEXT = ''
        self._poster = ''  # Ссылки на постер
        self._AGE_LIMIT = ''  # Возрастные ограничения

        self._production_year = ''  # Год производства
        self._episodes = ''  # Кол-во сезонов
        self._platform = ''  # Платформа
        self._country = ''  # Страна
        self._genre = ''  # Жанр
        self._tagline = ''  # Слоган
        self._director = ''  # Режиссер
        self._scenario = ''  # Сценарий
        self._producer = ''  # Продюсер
        self._operator = ''  # Оператор
        self._composer = ''  # Композитор
        self._designer = ''  # Художник
        self._edit = ''  # Монтаж
        self._budget = ''  # Бюджет
        self._marketing = ''  # Маркетинг
        self._US_fees = ''  # Сборы в США
        self._fees_in_the_world = ''  # Сборы в мире
        self._fees_in_Russia = ''  # Сборы в России
        self._premiere_in_Russia = ''  # Премьера в Росcии
        self._world_Premiere = ''  # Премьера в мире
        self._age = ''  # Возраст
        self._MPAA_rating = ''  # Рейтинг MPAA
        self._time = ''  # Время
        self._cast_list = ''  # Список Актеров
        self._film_sinopsis = ''  # Описание фильма
        self._rating = ''  # Рейтинг
        self._count_estimate = ''  # Кол-во оценок

        self._need_director = ''  # director link
        self._need_scenario = ''  # scenario link
        self._need_producer = ''  # producer link
        self._need_operator = ''  # operator link
        self._need_composer = ''  # composer link
        self._need_designer = ''  # designer link

        self.its_serial = False

    def _check_on_capcha(self):
        try:
            self._browser.refresh()
            self._browser.find_element(By.ID, 'js-button').click()
            print('Click to capcha')
            sleep(2)
        except:
            print('Capcha not found')
            sleep(3)

    def _get_title(self):
        try:
            pattern_film = '\ \(\d\d\d\d\)'
            try:
                text = self._browser.find_element(By.CLASS_NAME, 'styles_title__65Zwx').text
                self._TITLE = re.split(pattern_film, text)[0]
            except:
                text = self._browser.find_element(By.CLASS_NAME, 'styles_title___itJ6').text
                self._TITLE = re.split(pattern_film, text)[0]
        except:
            self._TITLE = ''

    def _get_age_limit(self):
        try:
            self._AGE_LIMIT = self._browser.find_element(By.CLASS_NAME, "styles_ageRate__340KC").text
        except:
            self._AGE_LIMIT = ''

    def _get_original_title(self):
        try:
            self._ORIGINAL_TITLE = self._browser.find_element(By.CLASS_NAME, 'styles_originalTitle__JaNKM').text
        except:
            self._ORIGINAL_TITLE = ''

    def _get_top_text(self):
        try:
            self._TOP_TEXT = browser.find_element(By.CLASS_NAME, 'styles_root__aZJRN').text
        except:
            self._TOP_TEXT = ''

    def _get_poster(self):
        try:
            try:
                self._browser.find_element(By.CLASS_NAME, 'styles_emptyPoster__oeGl_')
                self._poster = 'no-poster'
            except:
                # print('poster exist')
                try:
                    try:
                        a = self._browser.find_element(By.CLASS_NAME, 'styles_rootInLight__GwYHH')
                    except:
                        a = self._browser.find_element(By.CLASS_NAME, 'styles_rootInDark__64LVq')
                    # print('t: ',a.get_attribute("outerHTML"))
                    e = a.get_attribute("srcset").split()
                    self._poster = []
                    for i in e:
                        if i.startswith('//'):
                            r = i.replace('//', '')
                            self._poster.append(r)
                except:
                    # print('no poster')
                    self._poster = ''
        except:
            self._poster = ''

    def _get_information(self):
        list_of_elements = self._browser.find_elements(By.CSS_SELECTOR, ".styles_rowLight__P8Y_1")
        if not list_of_elements:
            list_of_elements = self._browser.find_elements(By.CSS_SELECTOR, ".styles_rowDark__ucbcz")

        for item in list_of_elements:
            # print('item: ', item.get_attribute("outerHTML"))
            if item.text.startswith('Год производства'):
                year_ep = item.find_elements(By.CSS_SELECTOR, "a")
                for i, elem in enumerate(year_ep):
                    if i == 0:
                        self._production_year = elem.text.strip()
                    if i == 1:
                        self._episodes = elem.text.strip()
            if item.text.startswith('Платформа'):
                self._platform = []
                res_pl = item.find_elements(By.CSS_SELECTOR, "a")
                for r in res_pl:
                    self._platform.append(r.text)

            if item.text.startswith('Страна'):
                self._country = []
                country = item.find_elements(By.TAG_NAME, "a")
                for r in country:
                    self._country.append(r.text)
            if item.text.startswith('Жанр'):
                self._genre = []
                genre = item.find_elements(By.TAG_NAME, "a")
                for r in genre:
                    if not r.text == 'слова':
                        self._genre.append(r.text)
            if item.text.startswith('Слоган'):
                self._tagline = item.find_element(By.CLASS_NAME, "styles_value__g6yP4").text

                # print('_tagline 3: ', self._tagline)

            if item.text.startswith('Режиссер'):
                self._director = []
                rej = item.find_elements(By.CSS_SELECTOR, "a")
                for r in rej:
                    if r.text == '...':
                        self._need_director = r.get_attribute("href")
                    else:
                        self._director.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Сценарий'):
                self._scenario = []
                res = item.find_elements(By.CSS_SELECTOR, "a")
                # print("res1:", res)
                for r in res:
                    if r.text == '...':
                        self._need_scenario = r.get_attribute("href")
                    else:
                        self._scenario.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Продюсер'):
                # print(item.text)
                self._producer = []
                res_p = item.find_elements(By.CLASS_NAME, "styles_link__3QfAk")
                # print("Прод1:", res_p)
                for r in res_p:
                    if r.text == '...':
                        self._need_producer = r.get_attribute("href")
                    else:
                        self._producer.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Оператор'):
                self._operator = []
                res_op = item.find_elements(By.CSS_SELECTOR, "a")
                for r in res_op:
                    if r.text == '...':
                        self._need_operator = r.get_attribute("href")
                    else:
                        self._operator.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Композитор'):
                self._composer = []
                res_c = item.find_elements(By.TAG_NAME, "a")
                for r in res_c:
                    if r.text == '...':
                        self._need_composer = r.get_attribute("href")
                    else:
                        self._composer.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Художник'):
                self._designer = []
                res = item.find_elements(By.TAG_NAME, "a")
                # print("Худ1:", res)
                for r in res:
                    if r.text == '...':
                        self._need_designer = r.get_attribute("href")
                    else:
                        self._designer.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Монтаж'):
                self._edit = []
                res_m = item.find_elements(By.CSS_SELECTOR, "a")
                for r in res_m:
                    self._edit.append({'name': r.text, 'link': r.get_attribute("href")})

            if item.text.startswith('Бюджет'):
                # self._budget = item.find_element(By.TAG_NAME, "a").text
                # ...
                # self._budget = []
                res_b = item.find_elements(By.CSS_SELECTOR, "a")
                for r in res_b:
                    self._budget = r.text

            if item.text.startswith('Маркетинг'):
                self._marketing = item.find_element(By.TAG_NAME, "a").text

            if item.text.startswith('Сборы в США'):
                self._US_fees = item.find_element(By.CSS_SELECTOR, "a").text

            if item.text.startswith('Сборы в мире'):
                self._fees_in_the_world = item.find_element(By.CSS_SELECTOR, "a").text

            if item.text.startswith('Сборы в России'):
                self._fees_in_Russia = item.find_element(By.CSS_SELECTOR, "a").text

            if item.text.startswith('Премьера в Росcии'):
                self._premiere_in_Russia = item.find_element(By.TAG_NAME, "a").text

            if item.text.startswith('Премьера в мире'):
                self._world_Premiere = item.find_element(By.TAG_NAME, "a").text

            if item.text.startswith('Возраст'):
                self._age = item.find_element(By.TAG_NAME, "a").text

            if item.text.startswith('Рейтинг MPAA'):
                self._MPAA_rating = item.find_element(By.CSS_SELECTOR, "a").text

            if item.text.startswith('Время'):
                try:
                    try:
                        self._time = item.find_element(By.CLASS_NAME, "styles_valueLight__nAaO3").text
                    except:
                        self._time = item.find_element(By.CLASS_NAME, "styles_valueDark__BCk93").text
                except:
                    self._time = ''

    def _get_cast(self):
        self._browser.get(self._link)
        if self._link == self._browser.current_url:
            self._cast_list = []
            try:
                list_persons = self._browser.find_elements(By.CLASS_NAME, "styles_link__Act80")
                count = self._browser.find_element(By.CLASS_NAME, "styles_moreItemsLink__hfZmk").text
                print('count: ', count)
                pat = '\ акт'
                self._count_actors = int(re.split(pat, count)[0])
                # print('co actors: ', self._count_actors)
                # print(list_persons[0])
                self._cast_list.append({'name': list_persons[0].text, 'link': list_persons[0].get_attribute("href")})
                # for i in list_persons:
                #     self._cast_list.append({'name': i.text, 'link': i.get_attribute("href")})
                # except:
                #     pass

                try:
                    self._browser.find_element(By.CLASS_NAME, "styles_moreItemsLink__hfZmk").click()
                except:
                    self._browser.find_element(By.CLASS_NAME, "styles_link__KtvyW").click()
                # self._cast_list = []
                actrs = self._browser.find_elements(By.CLASS_NAME, "actorInfo")
                self._flag = False
                for ii, act in enumerate(actrs):
                    name = act.find_element(By.CSS_SELECTOR, ".name>a")
                    if not self._flag:
                        if name.text == self._cast_list[0]['name']:
                            self._flag = True
                            continue
                    if self._flag:
                        if ii > self._count_actors:
                            # print('break i')
                            break
                        else:
                            self._cast_list.append({'name': name.text, 'link': name.get_attribute("href")})
            except:
                self._cast_list = ""
        else:
            self._check_on_capcha()
            sleep(1)
            self._get_cast()

    def _director_list(self):
        self._browser.get(self._need_director)
        if self._browser.current_url == self._need_director:
            actors = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._director = []
            for act1 in actors:
                name = act1.find_element(By.CSS_SELECTOR, ".name>a")
                self._director.append({'name': name.text, 'link': name.get_attribute("href")})

            self._need_director = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._director_list()

    def _scenario_list(self):
        self._browser.get(self._need_scenario)
        if self._browser.current_url == self._need_scenario:
            peopl_sc = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._scenario = []
            for act in peopl_sc:
                name = act.find_element(By.CSS_SELECTOR, ".name>a")
                self._scenario.append({'name': name.text, 'link': name.get_attribute("href")})
            self._need_scenario = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._scenario_list()

    def _producer_list(self):
        self._browser.get(self._need_producer)
        if self._browser.current_url == self._need_producer:
            peopl_sc = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._producer = []
            for act in peopl_sc:
                name = act.find_element(By.CSS_SELECTOR, ".name>a")
                self._producer.append({'name': name.text, 'link': name.get_attribute("href")})
            self._need_producer = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._producer_list()

    def _operator_list(self):
        self._browser.get(self._need_operator)
        if self._browser.current_url == self._need_operator:
            peopl_op = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._operator = []
            for act in peopl_op:
                name = act.find_element(By.CSS_SELECTOR, ".name>a")
                self._operator.append({'name': name.text, 'link': name.get_attribute("href")})
            self._need_operator = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._operator_list()

    def _composer_list(self):
        self._browser.get(self._need_composer)
        if self._browser.current_url == self._need_composer:
            peopl_com = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._composer = []
            for act in peopl_com:
                name = act.find_element(By.CSS_SELECTOR, ".name>a")
                self._composer.append({'name': name.text, 'link': name.get_attribute("href")})
            self._need_composer = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._composer_list()

    def _designer_list(self):
        self._browser.get(self._need_designer)
        if self._browser.current_url == self._need_designer:
            peopl_des = self._browser.find_elements(By.CLASS_NAME, "no_dub")
            self._designer = []
            for act in peopl_des:
                name = act.find_element(By.CSS_SELECTOR, ".name>a")
                self._designer.append({'name': name.text, 'link': name.get_attribute("href")})
            self._need_designer = ''
        else:
            self._check_on_capcha()
            sleep(1)
            self._designer_list()

    def _get_other_pages(self):
        if self._need_director:
            self._director_list()

        if self._need_scenario:
            self._scenario_list()

        if self._need_producer:
            self._producer_list()

        if self._need_operator:
            self._operator_list()

        if self._need_composer:
            self._composer_list()

        if self._need_designer:
            self._designer_list()

    def _get_film_sinopsis(self):
        try:
            self._film_sinopsis = self._browser.find_element(By.CLASS_NAME, "styles_filmSynopsis__Cu2Oz").text
        except:
            self._film_sinopsis = ''

    def _get_rating(self):
        try:
            # self._rating = self._browser.find_element(By.CLASS_NAME, "styles_ratingKpTop__84afd").text
            self._rating = self._browser.find_element(By.CLASS_NAME, "styles_rootLink__mm0kW").text
        except:
            self._rating = ''

        try:
            pat = "\ оцен"
            text = self._browser.find_element(By.CLASS_NAME, "styles_countBlock__jxRDI").text
            ress = re.split(pat, text)[0]
            self._count_estimate = ress.replace(' ', '')
        except:
            self._count_estimate = ''

    def _page_not_found(self):
        try:
            if self._browser.find_element(By.CLASS_NAME, "error-page__container-left"):
                return True
            else:
                return False
        except:
            return False

    def start(self):
        if self._page_not_found():
            logger.error(f"Page not found: {self._link}")
        else:
            sleep(1)
            self._get_title()
            self._get_top_text()
            self._get_original_title()
            self._get_poster()
            self._get_age_limit()
            self._get_information()
            self._get_rating()
            self._get_film_sinopsis()

            self._get_other_pages()
            self._get_cast()

            self._db.ADD_FILM(kp_id=self._id, full_link=self._link, title=self._TITLE,
                              origin_title=self._ORIGINAL_TITLE,
                              top_text=self._TOP_TEXT, poster=self._poster, year=self._production_year,
                              platform=self._platform, country=self._country, genre=self._genre, tagline=self._tagline,
                              director=self._director,
                              scenario=self._scenario, producer=self._producer, operator=self._operator,
                              composer=self._composer, designer=self._designer, edit=self._edit, budget=self._budget,
                              marketing=self._marketing,
                              US_fees=self._US_fees, fees_in_the_world=self._fees_in_the_world,
                              fees_in_Russia=self._fees_in_Russia, premiere_in_Russia=self._premiere_in_Russia,
                              world_Premiere=self._world_Premiere,
                              age=self._age, MPAA_rating=self._MPAA_rating, time=self._time, cast_list=self._cast_list,
                              film_sinopsis=self._film_sinopsis, rating=self._rating,
                              count_estimate=self._count_estimate)

    def run(self):
        sleep(1)
        if self._browser.current_url.startswith(f'{DOMAIN}series/'):
            logger.info(f"SERIAL_LINK: {self._link} #ID#")
            self.its_serial = True
        else:
            if self._browser.current_url.startswith(self._link):
                print('link == ')
                self.start()
            else:
                print('link != ')
                self._check_on_capcha()
                sleep(1)
                self.run()

    def result(self):
        print('Title: ', self._TITLE)
        print('Age limit: ', self._AGE_LIMIT)
        print('Original title: ', self._ORIGINAL_TITLE)
        print('Top text: ', self._TOP_TEXT)
        print('Logo: ', self._poster)
        print('Год производства: ', self._production_year)
        # print('Кол-во сезонов: ', self._episodes)
        print('Платформа: ', self._platform)
        print('Страна: ', self._country)
        print('Жанр: ', self._genre)
        print('Слоган: ', self._tagline)
        print('Режиссер: ', self._director)
        print('Сценарий: ', self._scenario)
        print('Продюсер: ', self._producer)
        print('Оператор: ', self._operator)
        print('Композитор: ', self._composer)
        print('Художник: ', self._designer)
        print('Монтаж: ', self._edit)
        print('Бюджет: ', self._budget)
        print('Маркетинг: ', self._marketing)
        print('Сборы в США: ', self._US_fees)
        print('Сборы в мире: ', self._fees_in_the_world)
        print('Сборы в России: ', self._fees_in_Russia)
        print('Премьера в Росcии: ', self._premiere_in_Russia)
        print('Премьера в мире: ', self._world_Premiere)
        print('Возраст: ', self._age)
        print('Рейтинг MPAA: ', self._MPAA_rating)
        print('Время: ', self._time)
        print('Актеры: ', self._cast_list)
        print('Описание фильма: ', self._film_sinopsis)
        print('Рейтинг фильма: ', self._rating)
        print('Кол-во оценок: ', self._count_estimate)


start = 235785
stop = 240000

for i in range(start, stop + 1):
    s = random.randrange(0, 2)
    print('\n ----------------------------------------------------------------------------------')
    print(f'Iteration {i} of {stop}. Жду: {s} секунд')
    sleep(s)
    rr = Get_Info_Film(browser=browser, link=DOMAIN + f'film/{i}/', id=i)
    rr.run()
    if rr.its_serial:
        continue
    rr.result()
