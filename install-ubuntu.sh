echo "Обновление пакетов"
sudo apt update > /dev/null

echo "Установка git & curl"
sudo apt install git curl> /dev/null

echo "Установка Heroku CLI"
curl https://cli-assets.heroku.com/install.sh | sh > /dev/null

heroku login

echo "Создание структуры проекта"
mkdir idm_lp
mkdir idm_lp/idm_lp
cd idm_lp || exit

curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/Procfile > Procfile
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/requirements.txt > requirements.txt
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/runtime.txt > runtime.txt

echo "Пожалуйста введите токен"
read token

echo '{"tokens": ["'$token'"]}' > idm_lp/config.json

echo "Пожалуйста введите имя приложения на Heroku"
read name

echo "Отправка файлов на сервер Heroku"
git init > /dev/null
heroku git:remote -a $name > /dev/null
git add . > /dev/null
git commit -am "make it better" > /dev/null
git push heroku master