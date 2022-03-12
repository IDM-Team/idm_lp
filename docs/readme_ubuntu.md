# Установка с Ubuntu (16.04+)

1. Открываем терминал
2. Вставляем следующие строки:
```bash
sudo apt install curl
curl https://raw.githubusercontent.com/IDM-Team/idm_lp/self-system-install/install-ubuntu.sh | sh
```


**Для обновления версии IDM LP:** `sudo service idmlp restart`

**Для обновления токенов:** изменяем файл `/root/idm_lp/config.json`