# Установка с Windows
1.Регистрируемся на [Heroku](https://heroku.com)
2. Переходим по [ссылке](https://dashboard.heroku.com/apps)
3. Создаем приложение, запоминаем его название
4. Скачиваем и устанавливаем [Git Bash](https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe)
5. Скачиваем и устанавливаем [Heroku CLI](https://cli-assets.heroku.com/heroku-x64.exe)
6. Нажимаем `Win`+`R` вводим `powershell`
7. Вводим следующюю строку:
```powershell
Set-ExecutionPolicy Unrestricted
```
8. Нажимаем `Y`, Перезагружаем ПК
9. Нажимаем `Win`+`R` вводим `powershell`
10. Вводим:
```powershell
$client = new-object System.Net.WebClient
mkdir -Path C:\IDMLP
$client.DownloadFile("https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/install-windows-heroku.ps1", "C:\IDMLP\installer.ps1")
Set-Location -Path "C:\IDMLP"
powershell -file "C:\IDMLP\installer.ps1"
```
11. Следуем инструкциям
12. Переходим по [ссылке](https://dashboard.heroku.com/apps)
13. Открываем свое приложение 
    1. Переходим во вкладку `Resources`
    2. Нажимаем на карандашик
    3. Нажимаем на переключатель
    4. Нажимаем `Confirm`
14. Наблюдаем работающий IDM LP
 
**Для обновления версии IDM LP:** 2 раза повторяем 13й шаг
 
**Для обновления токенов:** удаляем и устанавливаем приложение заново