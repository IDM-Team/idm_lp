# Установка с Termux

0. [Видео инструкция](https://vk.com/video-202354264_456239017)
1. Скачиваем APK с [репозитория](https://github.com/termux/termux-app/releases) universal.apk
2. Устанавливаем
3. Открываем, по порядку пишем команды:
```
pkg update -y
pkg upgrade -y
pkg install git python

git clone https://github.com/IDM-Team/idm_lp.git
cd idm_lp
git checkout heroku-deploy
nano idm_lp/config.json
```
4. Редактируем токены
5. Продолжаем вводить команды:
```
pip install -U idm_lp && python -m idm_lp --config_path idm_lp/config.json
```

**Для обновления версии IDM LP:** `pip install -U idm_lp`

**Для обновления токенов:** изменяем файл `idm_lp/config.json`

**Для запуска ЛП:**:
```
cd idm_lp
pip install -U idm_lp && python -m idm_lp --config_path idm_lp/config.json
```
