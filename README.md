# apps
- 1ое "уязвимое" приложение 
Брутфорс в логине
IDOR в профилях
Comand Injection через пинг
LFI через ссылку в профиле

Уязвимое приложение не имеет уязвимости SQLi. SQLite сразу экранирует параметры
Также не реализовано XSS

——————————————-

- 2ое приложение:
Пофиксино
LFI через приведение к каноническому виду os.path.basename
Comand Injection через отправку subprocess.check_output в виде списка, а не строки

Пыталась реализовать сессии, чтобы:
- капчу сделать от брутфорса. Но сессию можно проболжать использовать с тем же кодом, поэтому уязвимость не зафиксила
- от IDOR защититься

- Абстрактно, начала реализовывать подготовленные запросы для дополнительной защиты от SQLi
- +- нужна фильтрация от непредугаданных символов — в том числе будет защита от XSS, если бы была возможность
