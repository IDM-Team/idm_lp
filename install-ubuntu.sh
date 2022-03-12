echo "Обновление пакетов"
sudo apt update > /dev/null

echo "Установка python3.8"
if command -v python3.8 >/dev/null 2>&1
  then echo "python3.8 уже установлен"
  else
    sudo apt install -y build-essential zlib1g-dev libffi-dev libsqlite3-dev libncurses5-dev wget
    sudo apt install -y libncursesw5-dev libreadline6-dev libdb5.3-dev
    sudo apt install -y libgdbm-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev
    wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
    tar -xf Python-3.8.10.tgz
    rm Python-3.8.10.tgz
    cd Python-3.8.10 || exit
    ./configure --enable-optimizations
    sudo make altinstall
fi

python3.8 -m pip install -U pip

sudo mkdir /root/idm_lp

cd /root/idm_lp || exit

sudo python3.8 -m venv env

echo "Пожалуйста введите токен"

read token
echo '{"tokens": ["'$token'"]}' > /root/idm_lp/config.json

curl https://raw.githubusercontent.com/IDM-Team/idm_lp/self-system-install/idmlp.service > /etc/systemd/system/idmlp.service

sudo systemctl enable idmlp.service
sudo systemctl start idmlp.service

echo Это все