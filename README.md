# LAB 6 — Flask, SQLite, Docker, Nginx

![Jinja](https://img.shields.io/badge/jinja-%237E0C1B.svg?style=for-the-badge&logo=jinja&logoColor=white)
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%23499848.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%232496ED.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

Flask-застосунок для роботи з базою даних SQLite: студенти, дисципліни,
оцінки, середні бали, рейтинг, звіти ECTS, автентифікація користувачів із
серверними сесіями та CSRF-захистом. Проєкт запускається локально, у
Docker-контейнері або через Docker Compose у зв'язці Nginx + Gunicorn.

## Структура проєкту

```text
LAB6/
├── app.py              # Flask-застосунок і маршрути
├── db_init.py          # ініціалізація бази зі schema.sql і seed.sql
├── schema.sql          # структура таблиць
├── seed.sql            # початкові навчальні дані
├── create_user.py      # одноразове створення користувача
├── requirements.txt    # залежності Python (Flask, Gunicorn)
├── Dockerfile          # опис образу
├── compose.yaml        # Compose: backend (Gunicorn) + nginx
├── nginx.conf          # конфігурація Nginx для /etc/nginx/conf.d
├── .env.example        # шаблон змінних середовища без секретів
├── .dockerignore       # що не потрапляє в контекст збирання
├── .gitignore          # що не потрапляє в Git
├── templates/          # HTML-шаблони Jinja
├── instance/           # локальна база (не відстежується Git)
└── data/               # каталог даних для Docker (не відстежується Git)
```

## Вимоги до середовища

- Python 3.9 або новіший для локального запуску;
- Python 3.12 у Docker-образі;
- pip;
- Docker Desktop (перевірено на Docker 29.9.2);
- Docker Compose v2 (перевірено на v5.6.1);
- термінал: Terminal / iTerm на macOS, PowerShell або CMD на Windows.

Перевірити версії:

```bash
python3 --version
docker --version
docker compose version
```

Docker Desktop має бути запущений, інакше команди `docker` завершаться
помилкою підключення до демона.

## Швидкий старт через Docker Compose

Схема запиту:

```text
браузер -> 127.0.0.1:8080 -> Nginx :80 -> backend :5001 (Gunicorn)
```

1. Клонувати репозиторій і перейти в каталог:

```bash
git clone https://github.com/ytre12/WT-LAB6.git LAB6
cd LAB6
```

2. Підготувати `.env`:

```bash
cp .env.example .env
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Отримане значення вписати у `.env` замість `change-me`:

```text
SECRET_KEY=<згенероване_значення>
```

3. Перевірити конфігурацію, зібрати та запустити:

```bash
docker compose config --quiet
docker compose up --build -d
docker compose ps -a
```

Очікується: `backend` у стані `healthy`, `nginx` — `Up`, у Nginx
опублікований лише порт `127.0.0.1:8080->80/tcp`, у backend — `5001/tcp`
без адреси хоста.

4. Перевірити готовність:

```bash
curl -i http://127.0.0.1:8080/health
```

Очікується `HTTP/1.1 200 OK` і `{"status":"ok"}`.

5. Відкрити застосунок:

<http://127.0.0.1:8080/>

Демо-вхід:

| Логін | Пароль |
| --- | --- |
| `admin` | `Admin12345!` |
| `student` | `Student12345!` |
| `teacher` | `Teacher12345!` |

6. Переглянути журнали та перевірити синтаксис Nginx:

```bash
docker compose logs --tail=50 backend nginx
docker compose exec nginx nginx -t
```

7. Зупинити без втрати даних:

```bash
docker compose stop
```

`docker compose down` видаляє контейнери й мережу проєкту, але каталог
`./data` на хості залишається. Не використовувати `docker compose down -v`.

## Конфігурація середовища

| Змінна | Значення за замовчуванням | Призначення |
| --- | --- | --- |
| `SECRET_KEY` | немає, обов'язкова | ключ конфігурації застосунку |
| `PORT` | `5001` | порт, який слухає Flask або Gunicorn |
| `DATA_DIR` | `<проєкт>/instance` | каталог для файлу бази |
| `FLASK_DEBUG` | `0` | `1` вмикає режим налагодження |

`SECRET_KEY` зберігається лише у `.env`, який не потрапляє в Git. Шаблон без
робочого значення — `.env.example`. Значення має бути сталим між звичайними
перезапусками. `.env` не є зашифрованим сховищем секретів.

Compose автоматично читає `.env` для підстановки `${SECRET_KEY}`, а в
контейнер змінні передаються явно через `environment`.

## Локальний запуск

### macOS

```bash
cd /шлях/до/LAB6
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python3 -c 'import secrets; print(secrets.token_hex(32))'
# вписати отримане значення у .env замість change-me

set -a
source .env
set +a

python3 app.py
```

Відкрити: <http://127.0.0.1:5001>

### Windows

```powershell
cd C:\шлях\до\LAB6
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

py -c "import secrets; print(secrets.token_hex(32))"
$env:SECRET_KEY = "вставити_згенероване_значення"

py app.py
```

У CMD активація: `.venv\Scripts\activate.bat`.

Якщо PowerShell блокує скрипти:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Відкрити: <http://127.0.0.1:5001>

Приклад з іншим портом і каталогом даних:

```bash
set -a
source .env
set +a
PORT=8080 DATA_DIR="$PWD/instance" python3 app.py
```

> **Чому 5001, а не 5000.** На macOS порт 5000 часто займає AirPlay Receiver.
> Порт 5001 вільний.

## База даних та порядок ініціалізації SQLite

Застосунок використовує файл `app.sqlite3` у каталозі, який визначає
`DATA_DIR`. За замовчуванням це `instance/app.sqlite3`, а в Compose —
`/app/data/app.sqlite3`.

Під час старту застосунок виконує недеструктивну ініціалізацію:

1. створює каталог даних, якщо його немає;
2. виконує `schema.sql` із `CREATE TABLE IF NOT EXISTS`, тому наявні таблиці
   не перестворюються;
3. перевіряє в таблиці `app_meta` ознаку `seeded`;
4. якщо ознаки немає, виконує `seed.sql` і записує `seeded = 1`;
5. фіксує зміни через `commit`.

Повторний запуск не дублює записи й не повертає раніше видалені оцінки.
Окремого `flask init-db` у проєкті немає і він не потрібен.

Щоб використати готову базу, покладіть її як `app.sqlite3` у каталог даних:

```bash
mkdir -p data
cp шлях/до/app.sqlite3 data/app.sqlite3
```

Безпечна резервна копія SQLite:

```bash
sqlite3 data/app.sqlite3 ".backup 'data/backup.sqlite3'"
```

> Не копіюйте лише основний файл активної бази в режимі WAL. Для WAL також
> потрібні файли `-wal` і `-shm`, або коректний `.backup`.

## Облікові записи

Користувачі зберігаються в таблиці `users`. Пароль зберігається лише як хеш
із сіллю, створений `werkzeug.security`.

У початкових даних є демонстраційні записи:

| Логін | Пароль |
| --- | --- |
| `admin` | `Admin12345!` |
| `student` | `Student12345!` |
| `teacher` | `Teacher12345!` |

Це лише навчальні паролі. Для реального використання їх треба змінити, а
справжні секрети не додавати в репозиторій.

Новий користувач створюється одноразовим скриптом:

```bash
python3 create_user.py
```

## Docker без Compose

### Збирання образу

Версія інструменту: Docker 29.9.2. Тег образу: `flask-app:lab9`.

```bash
docker build -t flask-app:lab9 .
docker images flask-app:lab9
```

### Два варіанти відображення портів

1. Порт застосунку та порт хоста збігаються:

```bash
docker run -d --name flask-default \
  --env-file .env \
  -p 127.0.0.1:5001:5001 \
  flask-app:lab9
```

2. Порт застосунку змінено на 8080, хост — 5001:

```bash
docker run -d --name flask-data \
  --env-file .env \
  -e PORT=8080 \
  -p 127.0.0.1:5001:8080 \
  flask-app:lab9
```

Тут `PORT=8080` — порт усередині контейнера, `5001` — порт на хості.
Очікується `8080/tcp -> 127.0.0.1:5001`.

> У мапінгу `-p хост:контейнер` права частина завжди має збігатися з `PORT`
> у контейнері. Якщо залишити `-p 5001:5001` при `PORT=8080`, сторінка буде
> недоступною.

### Постійні дані

```bash
mkdir -p data

docker run -d --name flask-data \
  --env-file .env \
  -e PORT=8080 \
  -e DATA_DIR=/app/data \
  -p 127.0.0.1:5001:8080 \
  -v "${PWD}/data:/app/data" \
  flask-app:lab9
```

- `data/app.sqlite3` — файл бази на хості;
- `/app/data/app.sqlite3` — той самий файл у контейнері;
- якщо `data/` порожня, база створиться зі `schema.sql` і `seed.sql`;
- якщо в `data/` уже є `app.sqlite3`, застосунок використає його.

Перевірка:

```bash
docker logs flask-data
docker port flask-data
curl -i http://127.0.0.1:5001/
ls -l data
docker exec flask-data ls -l /app/data
docker inspect flask-data --format '{{json .Mounts}}'
```

У `Mounts` має бути `Source` — абсолютний шлях до `data/` на хості,
`Destination` — `/app/data`, `RW: true`.

### Повторний запуск зі збереженими даними

```bash
docker stop flask-data
docker rm flask-data

docker run -d --name flask-restored \
  --env-file .env \
  -e PORT=8080 \
  -e DATA_DIR=/app/data \
  -p 127.0.0.1:5001:8080 \
  -v "${PWD}/data:/app/data" \
  flask-app:lab9
```

Після повторного створення контейнера:

- студенти, дисципліни та оцінки залишаються в базі;
- сесії не зберігаються, бо живуть у пам'яті процесу, тому треба увійти
  повторно;
- нові записи, додані після повторного запуску, також зберігаються у
  `data/app.sqlite3`.

## Перевірка збереження після `docker compose down`

```bash
docker compose down
docker compose up -d
docker compose ps -a
curl -i http://127.0.0.1:8080/health
```

Після цього відкрити <http://127.0.0.1:8080/>, увійти повторно й перевірити
саме раніше створений запис: його ідентифікатор і вміст мають збігатися.
Існування файла `data/app.sqlite3` саме по собі не є доказом — потрібно
переконатися, що застосунок читає з нього дані.

Перевірка з хоста:

```bash
ls -l data/app.sqlite3
sqlite3 data/app.sqlite3 \
  "SELECT id, name FROM student ORDER BY id DESC LIMIT 5;"
```

## Архітектура Compose

- `backend` збирається з `Dockerfile`; Gunicorn слухає `0.0.0.0:5001`;
- `nginx` на образі `nginx:stable-alpine` проксіює запити на
  `http://backend:5001`;
- `nginx.conf` монтується в `/etc/nginx/conf.d/default.conf` у режимі `:ro`;
- каталог даних — `./data:/app/data`, `DATA_DIR=/app/data`;
- `SECRET_KEY` підставляється з `.env`;
- healthcheck звертається до `/health` усередині `backend` через
  `urllib.request`;
- використовується один worker, бо сесії зберігаються в пам'яті процесу.

Nginx передає `Host`, `X-Real-IP`, `X-Forwarded-For` і
`X-Forwarded-Proto`. Застосунок довіряє одному проксі через `ProxyFix`
(`x_for=1`, `x_proto=1`).

> Тег `nginx:stable-alpine` може змінюватися. Для точного відтворення
> зафіксуйте digest:
> `docker image inspect nginx:stable-alpine --format '{{index .RepoDigests 0}}'`.

## Діагностика

| Симптом | Причина | Що зробити |
| --- | --- | --- |
| `docker: Cannot connect to the Docker daemon` | Docker Desktop не запущений | Запустити Docker Desktop |
| `mapping key already defined` у Compose | порушені відступи YAML | вирівняти відступи, `docker compose config` |
| `Set SECRET_KEY in .env` | немає `.env` або ключа | створити `.env` з `SECRET_KEY` |
| `executable file not found: gunicorn` | не перезібрано образ | `docker compose build --no-cache` |
| `backend` постійно `unhealthy` | застосунок не слухає 5001 або падає | `docker compose logs backend` |
| `502 Bad Gateway` | різні порти в `proxy_pass` і `--bind` | узгодити `backend:5001` |
| `404` від Nginx | upstream відповів, але маршрут інший | перевірити шлях і логи backend |
| `port is already allocated` | порт 8080 зайнятий | змінити ліву частину `-p` |
| Файли не з'являються на хості | невірний `DATA_DIR` або монтування | перевірити `docker inspect` |
| Після змін нічого не оновилося | образ не перезібрано | `docker compose up --build -d` |

Корисні команди:

```bash
docker compose config --quiet
docker compose ps -a
docker compose logs --tail=100 backend nginx
docker compose exec nginx nginx -t
docker compose exec backend sh -c 'test -w /app/data && echo writable'
docker compose exec backend gunicorn --version
docker compose exec backend python -c 'import socket; print(socket.gethostbyname("backend"))'
docker compose exec backend python -c 'import urllib.request; print(urllib.request.urlopen("http://backend:5001/health", timeout=2).read().decode())'
```

Файли не з'являються на хості:

- перевірити `DATA_DIR`;
- перевірити `Mounts` через `docker inspect`;
- перевірити права доступу;
- не монтувати весь код поверх `/app`, якщо потрібен лише каталог даних.

На Linux із SELinux для виділеного каталогу може знадобитися:

```bash
-v "${PWD}/data:/app/data:Z"
```

Не використовувати `chmod 777` як спосіб обійти права. У rootless-режимі
окремо перевіряються права запису та зіставлення UID/GID.

Для віддаленого Docker-рушія джерела монтування `./data` і `./nginx.conf`
мають існувати на його хості.

## Podman (альтернатива)

```bash
podman build -f Dockerfile -t flask-app:lab9 .
podman run -d --name flask-data \
  --env-file .env \
  -e PORT=8080 -e DATA_DIR=/app/data \
  -p 127.0.0.1:5001:8080 \
  -v "${PWD}/data:/app/data" \
  flask-app:lab9
```

Для Podman правила `.dockerignore` слід продублювати в `.containerignore`.
У rootless-режимі окремо перевіряються права запису та UID/GID.

## Git і подання результатів

У репозиторій додаються:

- код застосунку та шаблони;
- `requirements.txt`, `Dockerfile`, `compose.yaml`, `nginx.conf`;
- `schema.sql`, `seed.sql`, `db_init.py`;
- `README.md`, `.env.example`, `.gitignore`, `.dockerignore`.

Не додаються:

- `.env` з робочим `SECRET_KEY`;
- `venv/`, `.venv/`, `__pycache__/`;
- `instance/`, `data/`, `logs/`;
- робочі файли SQLite;
- тестові `cookies.txt` і `login.html`.

Перевірка перед комітом:

```bash
git status --short
git check-ignore -v .env
git ls-files | grep -E '(^|/)(venv|\.venv)/|(^|/)\.env$'
```

Остання команда не повинна нічого вивести. Каталог `data/` з робочою базою
не входить у Git — його зберігають і подають окремо разом зі звітом.

## Приклад налаштувань із умовними значеннями

```bash
HOST_PORT="${HOST_PORT:-5001}"
APP_PORT="${APP_PORT:-8080}"
DATA_PATH="${DATA_PATH:-$PWD/data}"

mkdir -p "$DATA_PATH"

docker run -d --name flask-data \
  --env-file .env \
  -e PORT="$APP_PORT" \
  -e DATA_DIR=/app/data \
  -e FLASK_DEBUG=0 \
  -p "127.0.0.1:${HOST_PORT}:${APP_PORT}" \
  -v "${DATA_PATH}:/app/data" \
  flask-app:lab9
```

Справжні паролі, ключі та токени не додаються до репозиторію. Для локальних
експериментів використовуються лише демонстраційні значення; у production їх
передають через змінні середовища або менеджер секретів.

## Образ і контейнер: у чому різниця

- **Образ** `flask-app:lab9` — незмінний шаблон із кодом, залежностями та
  точкою входу. Він не містить робочої бази, бо `data/`, `instance/` і
  `*.sqlite3` виключені через `.dockerignore`.
- **Контейнер** — запущений екземпляр образу з власним процесом і тимчасовим
  шаром файлової системи. Без тому дані зникають після `docker rm`.
- **Том або bind-mount** — каталог на хості, який переживає видалення
  контейнера й забезпечує постійне зберігання даних.
