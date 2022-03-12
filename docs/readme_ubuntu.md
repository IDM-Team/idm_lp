# Установка с Ubuntu (16.04+)

1. Регистрируемся на [Heroku](https://heroku.com)
2. Переходим по [ссылке](https://dashboard.heroku.com/apps)
3. Создаем приложение, запоминаем его название
4. Открываем терминал
5. Вставляем следующие строки:
```bash
sudo apt install curl
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/install-ubuntu-heroku.sh | sh
```
6. Следуем инструкциям
7. Переходим по [ссылке](https://dashboard.heroku.com/apps)
8. Открываем свое приложение 
   1. Переходим во вкладку `Resources`
   2. Нажимаем на карандашик
   3. Нажимаем на переключатель
   4. Нажимаем `Confirm`
9. Наблюдаем работающий IDM LP

**Для обновления версии IDM LP:** 2 раза повторяем 8й шаг**

**Для обновления токенов:** удаляем и устанавливаем приложение заново