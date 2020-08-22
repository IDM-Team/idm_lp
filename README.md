### IDM multi - LP module
![Python version](https://img.shields.io/badge/python-3.7-blue)
![Version](https://img.shields.io/badge/version-1.3-blue)
![GitHub](https://img.shields.io/github/license/LordRalInc/idmmulti_lp)
![GitHub repo size](https://img.shields.io/github/repo-size/LordRalInc/idmmulti_lp)

LP модуль позволяет работать приемнику сигналов «IDM multi» работать в любых чатах.
Так же он добавляет игнор, глоигнор, мут и алиасы.

## Оглавление
1. [Установка](#установка)
2. [Аргументы запуска](#аргументы-запуска)
3. [Структура кофигурационного файла config.json](#структура-кофигурационного-файла-configjson)
4. [Команды модуля ЛП](#команды-модуля-лп)

## Установка
### Termux (Android)
Вводим по очереди команды
```shell script
pkg install git
pkg install python
git clone https://github.com/LordRalInc/idmmulti_lp.git
cd idmmulti_lp
pip install -r requirements.txt
nano config.json
```
Заполняем `config.json`
```shell script
Запуск:
python3 main.py
```
[![Установка IDM LP на Android (Termux)](https://img.youtube.com/vi/ULgyVBAXKqw/hqdefault.jpg)](https://youtu.be/ULgyVBAXKqw)

### Windows

Скачиваем и устанавливаем:
1. [Visual C++](https://support.microsoft.com/ru-ru/help/2977003/the-latest-supported-visual-c-downloads) (Если не установленно)
2. [Python](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)

Открываем CMD (Win + R и вводим cmd)
Вводим команды:
```shell script
cd путь_до_папки
py -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
```
Заполняем `config.json`
```shell script
Запуск:
cd путь_до_папки
env\Scripts\activate.bat
py main.py
```

### Linux (Ubuntu 16.04 Server)
```shell script
sudo apt-get update -y
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y

wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tar.xz
tar xf Python-3.7.7.tar.xz
cd Python-3.7.7
./configure
make -j {число ядер} && sudo make altinstall
```
`{число ядер}` можно узнать командой `nproc`
```shell script
sudo apt-get install git nano -y
git clone https://github.com/LordRalInc/idmmulti_lp.git
cd idmmulti_lp
nano config.json

python3.7 -m venv env
env/bin/python3.7 -m pip install -r requirements.txt
```
Создаем сервис для запуска
```shell script
nano /etc/systemd/system/idmlp.service
```
Вводим
```shell script
[Unit]
Description=LP
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/idmmulti_lp
ExecStart=/root/idmmulti_lp/env/bin/python3.7 /root/idmmulti_lp/main.py --config_path /root/idmmulti_lp/config.json

[Install]
WantedBy=multi-user.target
```
Нажимаем `ctrl + x` выходим
```shell script
systemctl enable idmlp
service idmlp start
```

## Аргументы запуска 
- `--logger_level [DEBUG | INFO | WARNING | ERROR | CRITICAL]` - Уровень логгирования
- `--config_path CONFIG_PATH` - Путь до файла с конфингом
- `--use_app_data` - Использовать папку AppData/IDM (Windows). При использовании этой настройки AppData/IDM и config_path складываются

## Структура кофигурационного файла config.json

- `tokens`            - Токены вк в количестве 3х штук. Получить можно [здесь](https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)
- `secret_code`       - Секретный код дежурного. Можно получить на странице настроек дежурного в графе `секретный код`
- `service_prefixes`  - Префиксы для выполнения команд модуля ЛП (добаление в мутлист, создание алиасов и тд.)
- `self_prefixes`     - Префиксы для высылки команд для себя (аналог !с .с ...)
- `duty_prefixes`     - Префиксы для высылки команд для дежурного (аналог !д .д ...)

**! Остальные поля заполняются программно**

![](https://sun1-86.userapi.com/10hU2v5Z8sV0ZBeDGWtOn4alEdiYZy2qY4_Ajw/_BeWOFmtcdw.jpg "Пример заполнения config.json")

## Команды модуля ЛП
- `{сервисный префикс}` пинг/кинг/пиу - пинг
- `{сервисный префикс}` инфо - информация о модуле ЛП
***
- `{сервисный префикс}` префиксы свои - просмотр своих префиксов
- `{сервисный префикс}` префиксы дежурный - просмотр префиксов для дежурного
- `{сервисный префикс}` +префикс `[свой/дежурный]` - создание префикса
- `{сервисный префикс}` -префикс `[свой/дежурный]` - удаление префикса
***
- `{сервисный префикс}` алиасы - просмотр алиасов
- `{сервисный префикс}` +алиас `{имя}` {enter} `{команда которую получает модуль ЛП}` {enter} `{команда которую отсылает модуль ЛП}`  - создание алиаса
- `{сервисный префикс}` -алиас `{имя}` - удаление алиаса
***
- `{сервисный префикс}` игнорлист - просмотр игнорлиста
- `{сервисный префикс}` +игнор `[{ссылка}/{упоминание}/{реплай}]` - добавить в игнорлист
- `{сервисный префикс}` -игнор `[{ссылка}/{упоминание}/{реплай}]` - удалить из игнорлиста
***
- `{сервисный префикс}` глоигнорлист - просмотр глоигнорлиста
- `{сервисный префикс}` +глоигнор `[{ссылка}/{упоминание}/{реплай}]` - добавить в глоигнорлист
- `{сервисный префикс}` -глоигнор `[{ссылка}/{упоминание}/{реплай}]` - удалить из глоигнорлиста
***
- `{сервисный префикс}` мутлист - просмотр мутлиста
- `{сервисный префикс}` +мут `[{ссылка}/{упоминание}/{реплай}]` - добавить в мутлист
- `{сервисный префикс}` -мут `[{ссылка}/{упоминание}/{реплай}]` - удалить из мутлиста






