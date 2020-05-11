# импорт библиотек
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


# главная функция
def main():
    # массив действий
    step = dict()

    # открыть сессию
    vk_session = vk_api.VkApi(
        token='4672e23f8c6f5a903b1bc27b081bd1525ba191a5d37aeaa1ef77ff885fd307b0764746032c0b28d608216')

    # открыть процесс
    longpoll = VkBotLongPoll(vk_session, 195023097)

    # перебрать события
    for event in longpoll.listen():

        # если событие - новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:

            # id пользователя отправившего сообщение
            peer_id = event.object.peer_id

            # обнуление всех действий для текущего пользователя
            try:
                step[peer_id] = step[peer_id]
            except KeyError:
                # массив действий (приветствие, как дела, погода)
                step[peer_id] = dict(hallo=0, tricks=0)

            # массив отправлений (тест, стикер)
            outer = dict(text="", sticker=0)

            # массив шаблонов фраз
            rubber = dict(
                how_are_you="Как дела?",
                talk_about_weather="Поговорим о погоде?\nСпросите меня: какая погода в...",
            )

            # тест полученного сообщения в нижнем регистре + удалить знаки пунктуации (!.?)
            inner = ''.join(c for c in event.object.text.lower() if c not in ('!', '.', '?'))

            # ВАРИАНТЫ ПРИВЕТСТВИЯ
            if inner in [
                'хелло',
                'привет',
                'здравствуйте',
            ]:

                # если это первое приветствие
                if not step[peer_id]['hallo']:
                    # дополнить исходящее сообщение
                    outer['text'] += "Здравствуйте, спасибо, что написали нам!\n"
                # если это повтроное приветствие
                else:
                    # прилепить стикер (хелло)
                    outer['sticker'] = 13699

                # отметить в массиве действий
                step[peer_id]['hallo'] += 1
                # дополнить исходящее сообщение
                outer['text'] += rubber['how_are_you']


            # ВАРИАНТЫ СОСТОЯНИЯ ДЕЛ (хорошие)
            elif inner in [
                'превосходно',
                'отлично',
                'хорошо',
            ]:

                # если это первое сообщение о состоянии дел
                if not step[peer_id]['tricks']:
                    # дополнить исходящее сообщение
                    outer['text'] += "Приятно, когда у человека всё хоршо!\n"
                # если это повтроное сообщение о состоянии дел
                else:
                    # прилепить стикер (лойс)
                    outer['sticker'] = 13710

                # отметить в массиве действий
                step[peer_id]['tricks'] += 1
                # дополнить исходящее сообщение
                outer['text'] += rubber['talk_about_weather']

            # ВАРИАНТЫ СОСТОЯНИЯ ДЕЛ (нейтральные)
            elif inner in [
                'нормально',
                'норм',
                'никак',
                'не плохо',
            ]:

                # если это первое сообщение о состоянии дел
                if not step[peer_id]['tricks']:
                    # дополнить исходящее сообщение
                    outer['text'] += "Отлично! Эмоциональная стабильность повышает работоспособность.\n"
                # если это повтроное сообщение о состоянии дел
                else:
                    # прилепить стикер (щёлк-щёлк)
                    outer['sticker'] = 13701

                # отметить в массиве действий
                step[peer_id]['tricks'] += 1
                # дополнить исходящее сообщение
                outer['text'] += rubber['talk_about_weather']

            # ВАРИАНТЫ СОСТОЯНИЯ ДЕЛ (плохие)
            elif inner in [
                'отвратительно',
                'плохо',
                'не очень',
            ]:
                # создать пустое исходящее сообщение
                outer['text'] = ""

                # если это первое сообщение о состоянии дел
                if not step[peer_id]['tricks']:
                    # дополнить исходящее сообщение
                    outer['text'] += "Не расстраивайтесь, всё образуется!\n"
                # если это повтроное сообщение о состоянии дел
                else:
                    # прилепить стикер (иди обниму)
                    outer['sticker'] = 13746

                # отметить в массиве действий
                step[peer_id]['tricks'] += 1
                # дополнить исходящее сообщение
                outer['text'] += rubber['talk_about_weather']

            # ОСТАЛЬНЫЕ СООБЩЕНИЯ (включая погоду)
            else:

                # шаблон фразы о погоде
                pattern = 'какая погода в '
                # найти подстроку в полученном сообщении
                weather = inner.find(pattern)

                # если подстрока найдена
                if weather > -1:
                    # получить название города, удалив подстроку-шаблон
                    city = inner.replace(pattern, '')
                    # обрезать крайние пробелы
                    city = city.strip()
                    # написать город с заглавной буквы
                    city = city.title()

                    # ЗАПРОС ПОГОДЫ В ГОРОДЕ
                    if city != '':
                        # запросить погоду и создать из ответа исходящее сообщение
                        outer['text'] = get_weather(city)

                    # если город пустой
                    else:
                        weather = -1

                # ОСТАЛЬНЫЕ СООБЩЕНИЯ
                if weather < 0:

                    # импорт библиотек
                    import re
                    # сократить много скобок до одной
                    smile = re.sub(r'(\))\1+', r'\1', inner)
                    # если сообщение это "улыбающаяся" скобка
                    if smile == ')':
                        # прилепить стикер (смайл)
                        outer['sticker'] = 13715

                    # если приветствия не было
                    elif not step[peer_id]['hallo']:
                        # прилепить стикер (хелло)
                        outer['sticker'] = 13699

                    # если нет ответа как дела
                    elif not step[peer_id]['tricks']:
                        # создать исходящее сообщение
                        outer['text'] = rubber['how_are_you']

                    # ВСЕ ДРУГИЕ ФРАЗЫ И СОСТОЯНИЯ
                    else:
                        # прилепить стикер (бла-бла-бла)
                        outer['sticker'] = 13711
                        # создать исходящее сообщение
                        outer['text'] += rubber['talk_about_weather']

            # сессия
            vk = vk_session.get_api()
            # если прилеплен стикер - отобразить
            if outer['sticker']:
                vk.messages.send(user_id=event.object.peer_id,
                                 sticker_id=outer['sticker'],
                                 random_id=random.randint(0, 2 ** 64))

            # если сформировано сообщение - отобразить
            if outer['text']:
                vk.messages.send(user_id=event.object.peer_id,
                                 message=outer['text'],
                                 random_id=random.randint(0, 2 ** 64))


# программа - запрос координат города и погоды
def get_weather(city):
    # импорт библиотек
    import requests
    import json

    # запрос к Яндекс-Геокодеру для получения координат по названию города
    try:
        ya_geocode = requests.get(
            'https://geocode-maps.yandex.ru/1.x/?apikey=694e628e-f295-493c-870e-9844b0773310&geocode=' + city + '&results=1&lang=ru_RU&format=json')
        # раскодировать json
        ya_geocode = json.loads(ya_geocode.content)
        # добраться до списка результатов
        ya_geocode = ya_geocode['response']['GeoObjectCollection']['featureMember']

        # если результат есть
        if len(ya_geocode):
            geo = ya_geocode[0]['GeoObject']
            # полное название города
            city = geo['name'] + ", " + geo['description']
            # координаты города
            geo = "lon=" + geo['Point']['pos'].replace(' ', '&lat=')

        # если результата нет - вернуть сообщение
        else:
            return "Не удалось найти в справочнике город «" + city + "»"

        # запрос к Яндекс-Погоде для получения погоды по координатам
        try:
            ya_weather = requests.get(
                'https://api.weather.yandex.ru/v1/forecast?' + geo + '&limit=1&hours=false&lang=ru_RU',
                headers={'X-Yandex-API-Key': '39dd2806-fcd9-41b5-84e5-2e71f147fe14'}
            )
            # раскодировать json
            ya_weather = json.loads(ya_weather.content)
            # погода на данный момент
            fact = ya_weather['fact']

            # создать исходящее сообщение
            out = city + ", сейчас:\n"
            # температура
            if fact['temp'] >= 0:
                fact['temp'] = "+" + str(fact['temp'])
            out += "Температура воздуха: " + str(fact['temp']) + "\n"
            # ощущается
            if fact['feels_like'] >= 0:
                fact['feels_like'] = "+" + str(fact['feels_like'])
            out += "Ощущается как: " + str(fact['feels_like']) + "\n"
            # направление ветра
            if fact['wind_dir'] == 'n':
                fact['wind_dir'] = "северный"
            if fact['wind_dir'] == 'ne':
                fact['wind_dir'] = "северо-восточный"
            if fact['wind_dir'] == 'e':
                fact['wind_dir'] = "восточный"
            if fact['wind_dir'] == 'se':
                fact['wind_dir'] = "юго-восточный"
            if fact['wind_dir'] == 's':
                fact['wind_dir'] = "южный"
            if fact['wind_dir'] == 'sw':
                fact['wind_dir'] = "юго-западный"
            if fact['wind_dir'] == 'w':
                fact['wind_dir'] = "западный"
            if fact['wind_dir'] == 'nw':
                fact['wind_dir'] = "северо-западный"
            # скорость ветра
            if fact['wind_speed']:
                out += "Ветер " + fact['wind_dir'] + " " + str(fact['wind_speed']) + " м/с\n"
            else:
                outer += "Ветра нет\n"
            # давление
            out += "Атмосферное давление: " + str(fact['pressure_mm']) + " мм/р.с\n"
            # вернуть сообщение
            return out

        # ошибка при получении данных о погоде
        except Exception as e:
            return "Сервис погоды в данный момент недоступен, спросите меня об этом позже"
    # ошибка при получении координат города
    except Exception as e:
        return "Не удалось разобрать какой город вы имеете ввиду: «" + city + "»"


# запустить главную программу
if __name__ == '__main__': main()
