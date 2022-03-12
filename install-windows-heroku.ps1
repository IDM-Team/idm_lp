Write-Host Начинаю загрузку данных для IDM LP

$client = new-object System.Net.WebClient
Set-Location -Path "C:\IDMLP"
mkdir -Path "C:\IDMLP\idm_lp"


$procfileUrl = "https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/Procfile"
$requirementsUrl = "https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/requirements.txt"
$runtimeUrl = "https://raw.githubusercontent.com/IDM-Team/idm_lp/heroku-deploy/runtime.txt"

$client.DownloadFile(
    $procfileUrl,
    "C:\IDMLP\Procfile"
)
$client.DownloadFile(
    $requirementsUrl,
    "C:\IDMLP\requirements.txt"
)
$client.DownloadFile(
    $runtimeUrl,
    "C:\IDMLP\runtime.txt"
)

$token = Read-Host Введите токен от VK
$herokuAppName = Read-Host Введите имя приложения Heroku

heroku login

$config = '{"tokens": ["' + $token + '"]}'

Out-File -FilePath "C:\IDMLP\idm_lp\config.json" -InputObject $config

git init
heroku git:remote -a $herokuAppName
git add .
git commit -am "make it better"
git push heroku master