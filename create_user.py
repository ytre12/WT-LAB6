"""Одноразове створення облікового запису в таблиці users.

Запуск:
    python3 create_user.py

Скрипт запитує логін і пароль, обчислює хеш і додає користувача в points.db.
Після створення потрібних записів цей файл можна видалити.
"""

from getpass import getpass

from werkzeug.security import check_password_hash, generate_password_hash

from app import app, get_db


def hash_password(password):
    """Повертає хеш пароля з сіллю.

    scrypt потребує OpenSSL з підтримкою scrypt; якщо його немає
    (наприклад, у системному Python 3.9 на macOS), використовуємо PBKDF2.
    """
    try:
        return generate_password_hash(password, method="scrypt")
    except (AttributeError, ValueError):
        return generate_password_hash(password, method="pbkdf2:sha256")


def create_account(db, username, password):
    """Додає користувача й повертає його id."""
    password_hash = hash_password(password)
    assert check_password_hash(password_hash, password)

    try:
        cur = db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return cur.lastrowid


def main():
    username = input("Логін: ").strip()
    password = getpass("Пароль: ")
    confirmation = getpass("Повторіть пароль: ")

    if not username or not password or password != confirmation:
        raise ValueError("Перевірте логін і підтвердження пароля")

    with app.app_context():
        db = get_db()

        if db.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        ).fetchone() is None:
            raise SystemExit(
                "Таблиці users немає. Створіть її запитом з умови лабораторної."
            )

        try:
            user_id = create_account(db, username, password)
        except Exception as exc:
            raise SystemExit(f"Не вдалося створити користувача: {exc}") from exc

    print(f"Користувача {username!r} створено (id={user_id}).")


if __name__ == "__main__":
    main()
