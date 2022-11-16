# Чат бот с информацией о ТВ программе

## TgBot

Реализован класс TgBot, который позволяет создавать инстансы ботов, которые могут отправлять сообщения в чаты и получать
сообщения из чатов.

### Доступный функционал:

* **send_message(chat_id, text, parse_mode)** - отправляет сообщение в чат с chat_id, содержащее текст text, с
  возможностью
  выбора режима разметки текста (по умолчанию - MarkdownV2)

* **get_updates()** - возвращает список обновлений, которые были получены с момента последнего вызова этого метода

* **add_handler(handler)** - добавляет обработчик handler, который будет вызываться при получении сообщения,
  удовлетворяющего
  условиям, заданным в handler

* **run()** - запускает бесконечный цикл, в котором бот получает обновления и обрабатывает их

* **stop()** - останавливает бесконечный цикл, запущенный методом run()

## Базовая логика работы

При текстовом сообщении от пользователя бот делает запрос к API сайта [tvmaze.com](tvmaze.com) и получает информацию о
сериале, который пользователь ищет. После этого бот отправляет пользователю сообщение с информацией о сериале.

При нетекстовом сообщении выдается ошибка.

Пример работы бота:

```
# запускаем бота
python -m main.py
```

```
# чат в телеграм
User:

Family Guy

Bot:

Name: Family Guy
Network Name: FOX
Network Country Name: United States
Summary: Family Guy follows Peter Griffin the endearingly ignorant dad, and his hilariously offbeat family of middle-class New Englanders in Quahog, RI. Lois is Peter's wife, a stay-at-home mom with no patience for her family's antics. Then there are their kids: 18-year-old Meg is an outcast at school and the Griffin family punching bag; 13-year-old Chris is a socially awkward teen who doesn't have a clue about the opposite sex; and one-year-old Stewie is a diabolically clever baby whose burgeoning sexuality is very much a work in progress. Rounding out the Griffin household is Brian the family dog and a ladies' man who is one step away from AA.
```

## Усложненный вариант

Реализована логика:

* Добавления шоу в избранное командой
    * **/add_to_favorites [program_name]**
* Вывода списка избранных шоу
    * **/get_favorites**
* Удаления шоу из избранного
    * **/remove_from_favorites [program_name]**

Шоу сохраняется посредством `FileDict`.

## Критерии оценивания

1) Сделать клиент для API телеграма - 2 балла - **Done**
2) Сделать бота, который реализует логику общения - 2 балла - **Done**
3) Сделать скрипт, который запускает бота для обработки входящих сообщений - 2 балла - **Done**
4) Использовать изученные методики ООП (создать логические классы, сделать релевантные методы для их работы) - 2 балла - **Probably Done**
5) Пройти проверку линтерами - 1 балл - **Done**
6) Покрыть тестами логику работы бота - 1 балл - **Done**
7) Реализовать логику избранного шоу - отдельные доп 3 балла - **Probably Done**
 
 