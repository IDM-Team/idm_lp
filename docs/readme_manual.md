# Ручная установка

1. Регистрируемся на [GitHub](https://github.com)(Вы сейчас на нем)
2. Создаем закрытый репозиторий, название любое, потом заходим в этот репозиторий
3. Внизу будет «import code», нажимаем туда и вставляем в окошко ссылку `https://github.com/IDM-Team/idm_lp`
4. Импортируем (нажимаем кнопку `begin import`)
5. Далее заходим в этот репозиторий, меняем «master» на «heroku-deploy» 
6. Заходим в папку `idm_lp`, следом в файлик `config.json`
7. Жмём на карандашик (три точки - `edit file`)
8. В квадратные скобки вводим токен от Kate Mobile: `["в кавычках вставляем обрезанный токен"]`
9. Дальше листаем вниз и сохраняем 
10. Регистрируемся на [Heroku](https://heroku.com), при регистрации нужно выбрать язык `«python»`
11. Создаете приложение (выбрать `Europe`), заходите в него и подключаетесь к GitHub. 
12. В `repo-name` пишем название репозитория с GitHub (`search` -> `connect`)
13. `master` меняем на `heroku-deploy`. 
14. Нажимаем на `deploy branch`
15. Ждём окончания деплоя 
16. После окончания деплоя листаем вверх и нажимаем на `resources` (второй значок из трёх полосочек)
17. Обновляем страницу, там появится модуль. 
18. Нажимаем на карандашик, потом на ползунок и «confirm» 
19. После сообщений о запуске пишем:
`.слп получить бд`
 
**Для обновления версии IDM LP:** 2 раза повторяем 16-18 шаги
 
**Для обновления токенов:** изменяем файл `config.json`, деплоим