# LAB 6 — Flask, SQLite, Docker

![Jinja](https://img.shields.io/badge/jinja-%237E0C1B.svg?style=for-the-badge&logo=jinja&logoColor=white)
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%232496ED.svg?style=for-the-badge&logo=docker&logoColor=white)

Flask-застосунок для роботи з базою даних SQLite: студенти, дисципліни,
оцінки, середні бали, рейтинг, звіти ECTS, автентифікація користувачів із
серверними сесіями та CSRF-захистом. Проєкт підготовлено до запуску локально
та в Docker-контейнері.

## Структура проєкту

```text
LAB6/
├── app.py              # Flask-застосунок і маршрути
├── db_init.py          # ініціалізація бази зі schema.sql і seed.sql
├── schema.sql          # структура таблиць
├── seed.sql            # початкові навчальні дані
├── create_user.py      # одноразове створення користувача
├── requirements.txt    # залежності Python
├── Dockerfile          # опис образу
├── .dockerignore       # що не потрапляє в контекст збирання
├── .gitignore          # що не потрапляє в Git
├── templates/          # HTML-шаблони Jinja
├── instance/           # локальна база (не відстежується Git)
└── data/               # каталог даних для Docker (не відстежується Git)
```

## Вимоги

- Python 3.9 або новіший для локального запуску;
- Python 3.12 у Docker-образі;
- pip;
- Docker Desktop (перевірено на Docker 29.9.2);
- термінал: Terminal / iTerm на macOS, PowerShell або CMD на Windows.

Перевірити версії:

```bash
python3 --version
docker --version
```

## Локальний запуск

### macOS

```bash
cd /шлях/до/LAB6
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Відкрити: <http://127.0.0.1:5001>

### Windows

```powershell
cd C:\шлях\до\LAB6
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

У CMD активація: `.venv\Scripts\activate.bat`.

Якщо PowerShell блокує скрипти:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Відкрити: <http://127.0.0.1:5001>

### Конфігурація локального запуску

| Змінна | Значення за замовчуванням | Призначення |
| --- | --- | --- |
| `PORT` | `5001` | порт, який слухає Flask |
| `DATA_DIR` | `<проєкт>/instance` | каталог для файлу бази |
| `FLASK_DEBUG` | `0` | `1` вмикає режим налагодження |

Приклад:

```bash
PORT=8080 DATA_DIR="$PWD/instance" python3 app.py
```

> **Чому 5001, а не 5000.** На macOS порт 5000 часто займає AirPlay Receiver.
> Порт 5001 вільний.

## База даних та порядок ініціалізації SQLite

Застосунок використовує файл `app.sqlite3` у каталозі, який визначає
`DATA_DIR`. За замовчуванням це `instance/app.sqlite3`.

Під час старту `app.py` викликає `ensure_database()` з `db_init.py`, який
працює так:

1. створює каталог даних, якщо його немає;
2. виконує `schema.sql` із `CREATE TABLE IF NOT EXISTS`, тому наявні таблиці
   не перестворюються;
3. перевіряє в таблиці `app_meta` ознаку `seeded`;
4. якщо ознаки немає, виконує `seed.sql` і записує `seeded = 1`;
5. фіксує зміни через `commit`.

Така ініціалізація є недеструктивною: повторний запуск не дублює записи й не
повертає раніше видалені оцінки. Окремого `flask init-db` у проєкті немає і
він не потрібен.

Щоб використати готову базу з матеріалів лабораторної, покладіть її як
`app.sqlite3` у каталог даних:

```bash
mkdir -p instance
cp points.db instance/app.sqlite3
```

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

## Docker: збирання образу

Версія інструменту: Docker 29.9.2. Тег образу: `flask-app:lab9`.

```bash
docker build -t flask-app:lab9 .
```

Перевірити образ:

```bash
docker images flask-app:lab9
```

## Docker: два варіанти відображення портів

### 1. Порт застосунку та порт хоста збігаються

Застосунок слухає 5001 у контейнері, на хості також 5001:

```bash
docker run -d --name flask-default \
  -p 127.0.0.1:5001:5001 \
  flask-app:lab9
```

Перевірка:

```bash
docker port flask-default
curl -i http://127.0.0.1:5001/
```

### 2. Порт застосунку змінено на 8080, хост — 5001

```bash
docker run -d --name flask-data \
  -e PORT=8080 \
  -p 127.0.0.1:5001:8080 \
  flask-app:lab9
```

Тут `PORT=8080` — порт усередині контейнера, `5001` — порт на хості.
Очікується `8080/tcp -> 127.0.0.1:5001`.

> У мапінгу `-p хост:контейнер` права частина завжди має збігатися з `PORT`
> у контейнері. Якщо залишити `-p 5001:5001` при `PORT=8080`, сторінка буде
> недоступною.

## Docker: постійні дані

Каталог даних на хості монтується в контейнер як `/app/data`:

```bash
mkdir -p data

docker run -d --name flask-data \
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

## Docker: повторний запуск зі збереженими даними

```bash
docker stop flask-data
docker rm flask-data

docker run -d --name flask-restored \
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

Зупинка без видалення даних:

```bash
docker stop flask-restored
```

Каталог `data/` після цього зберігається для подання результатів.

## Приклад налаштувань із умовними значеннями

```bash
HOST_PORT="${HOST_PORT:-5001}"
APP_PORT="${APP_PORT:-8080}"
DATA_PATH="${DATA_PATH:-$PWD/data}"

mkdir -p "$DATA_PATH"

docker run -d --name flask-data \
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

## Діагностика

Контейнер не запускається:

```bash
docker ps -a
docker logs flask-restored
```

Перевірити залежності, точку входу, `PORT` і наявність схеми БД.

Сторінка недоступна:

```bash
docker port flask-restored
```

Зіставити `PORT` у контейнері з правою частиною `-p`. Якщо порт хоста
зайнятий, змінити ліву частину, залишивши праву без змін.

Файли не з'являються на хості:

- перевірити `DATA_DIR`;
- перевірити `Mounts` через `docker inspect`;
- перевірити права доступу;
- не монтувати весь код поверх `/app`, якщо потрібен лише каталог даних.

На Linux із SELinux для виділеного каталогу може знадобитися:

```bash
-v "${PWD}/data:/app/data:Z"
```

Не використовувати `chmod 777` як спосіб обійти права.

## Podman (альтернатива)

```bash
podman build -f Dockerfile -t flask-app:lab9 .
podman run -d --name flask-data \
  -e PORT=8080 -e DATA_DIR=/app/data \
  -p 127.0.0.1:5001:8080 \
  -v "${PWD}/data:/app/data" \
  flask-app:lab9
```

Для Podman правила `.dockerignore` слід продублювати в `.containerignore`.
У rootless-режимі окремо перевіряються права запису та UID/GID.

## Що не потрапляє в Git і Docker

`.gitignore` виключає `venv/`, `.venv/`, `__pycache__/`, `instance/`, `data/`,
`logs/`, `*.db`, `*.sqlite*`, `.env*`, тестові `cookies.txt` і `login.html`.

`.dockerignore` додатково не пропускає в контекст збирання `.git/`, локальні
середовища Python, секрети й робочі бази, але залишає `schema.sql` і
`seed.sql`.
