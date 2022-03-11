sudo apt update
sudo apt install git curl
curl https://cli-assets.heroku.com/install.sh | sh
heroku login

mkdir idm_lp
mkdir idm_lp/idm_lp
cd idm_lp || exit

curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/Procfile > Procfile
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/requirements.txt > requirements.txt
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/runtime.txt > runtime.txt

echo Пожалуйста введите токен
read token

echo '{"tokens": ["'$token'"]}' > idm_lp/config.json

echo Пожалуйста введите имя приложения на Heroku
read name
git init
heroku git:remote -a $name
git add .
git commit -am "make it better"
git push heroku master