# LAB 6

![Jinja](https://img.shields.io/badge/jinja-%237E0C1B.svg?style=for-the-badge&logo=jinja&logoColor=white)
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)

Flask-застосунок для роботи з базою даних `points.db` (SQLite)

## Вимоги

- Python 3.9 або новіший
- pip (встановлюється разом із Python)
- термінал: Terminal / iTerm на macOS, PowerShell або CMD на Windows

Перевірити версію Python:

```bash
python3 --version    # macOS
py --version         # Windows
```

## База даних

Для роботи застосунку **обов'язково потрібен файл бази даних `points.db`**.
Його можна взяти з матеріалів до лабораторної роботи. Файл потрібно покласти
в корінь проєкту — поруч із `app.py`.

```text
LAB6/
├── app.py
├── points.db        ← покласти сюди
├── requirements.txt
└── templates/
```

Застосунок **не створює** базу й таблиці сам: він розраховує, що в `points.db`
уже є таблиці `student`, `course` і `points`. Якщо файлу немає, сторінки
завершаться помилкою `no such table`.

База не зберігається в Git (вона є в `.gitignore`), тому після клонування
репозиторію файл `points.db` потрібно скопіювати вручну з матеріалів
лабораторної роботи.

## macOS

1. Перейдіть у теку проєкту:

   ```bash
   cd /шлях/до/LAB6
   ```

2. Створіть віртуальне середовище:

   ```bash
   python3 -m venv .venv
   ```

3. Активуйте його:

   ```bash
   source .venv/bin/activate
   ```

   У рядку термінала має з'явитися префікс `(.venv)`.

4. Встановіть залежності:

   ```bash
   pip install -r requirements.txt
   ```

5. Запустіть сервер:

   ```bash
   python3 app.py
   ```

6. Відкрийте у браузері:

   ```text
   http://127.0.0.1:5001
   ```

> **Чому порт 5001, а не 5000.** На macOS порт 5000 займає служба AirPlay
> (Receiver), тому застосунок на ньому не запуститься або віддаватиме
> помилку 403. Порт 5001 вільний.

## Windows

1. Перейдіть у теку проєкту:

   ```powershell
   cd C:\шлях\до\LAB6
   ```

2. Створіть віртуальне середовище:

   ```powershell
   py -m venv .venv
   ```

   Якщо команда `py` недоступна, використайте `python -m venv .venv`.

3. Активуйте середовище.

   **PowerShell:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **CMD:**

   ```bat
   .venv\Scripts\activate.bat
   ```

4. Якщо PowerShell блокує запуск скриптів, дозвольте його лише для поточного
   сеансу:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

   Після цього повторіть активацію. Системні налаштування не змінюються.

5. Встановіть залежності:

   ```powershell
   pip install -r requirements.txt
   ```

6. Запустіть сервер:

   ```powershell
   py app.py
   ```

7. Відкрийте у браузері:

   ```text
   http://127.0.0.1:5001
   ```

## Зупинка сервера

У терміналі з запущеним Flask натисніть `Ctrl+C`.

## Сторінки застосунку

| Адреса | Призначення |
| --- | --- |
| `/` | список студентів |
| `/courses` | список дисциплін |
| `/all_grades` | усі оцінки; редагування та видалення |
| `/grades/new` | додавання оцінки |
| `/grades/<id>/edit` | редагування оцінки |
| `/grades/<id>/delete` | видалення оцінки (лише POST) |
| `/student/<id>/grades` | оцінки конкретного студента |
| `/rating/<course_id>/rating` | рейтинг студентів за дисципліною |
| `/courses/avg` | середній бал за кожною дисципліною |
| `/course/ects` | розподіл оцінок за шкалою ECTS для дисциплін |
| `/students/ects` | розподіл оцінок за ECTS для студентів і семестрів |

## Де зберігаються дані

Усі дані зберігаються в одному файлі SQLite — `points.db` у корені проєкту.
Окремі файли для кожного запису не створюються. Зміни вносяться запитами
`INSERT`, `UPDATE` і `DELETE` у таблицю `points`; семестр береться з таблиці
`course`, тому окремо в `points` він не зберігається.

## Що не потрапляє в Git

У репозиторії зберігається лише код. Завдяки `.gitignore` не відстежуються:

- `venv/` і `.venv/` — віртуальні середовища;
- `points.db` та інші файли `*.db`/`*.sqlite` — база даних;
- `__pycache__/` і `*.pyc` — кеш Python;
- `.env`, `.DS_Store`, `.vscode/`, `.idea/`.

Тому після клонування репозиторію потрібно самостійно створити віртуальне
середовище, встановити залежності та скопіювати `points.db`.
