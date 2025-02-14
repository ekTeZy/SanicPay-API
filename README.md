# SanicPay API

## Описание
SanicPay - API с использованием **Sanic**, **PostgreSQL**, **SQLAlchemy** и **Alembic**. В проекте поддерживается запуск через Docker и локально.

---

## Запуск через Docker
### **1. Убедитесь, что установлен Docker и Docker Compose**

- **Проверьте версию Docker**
  ```sh
  docker --version
  ```
- **Проверьте версию Docker Compose**
  ```sh
  docker-compose --version
  ```

### **2. Клонируйте репозиторий**
```sh
 git clone https://github.com/ekTeZy/SanicPay-API.git
 cd SanicPay-API
```

### **3. Запустите проект через Docker**
```sh
docker-compose up --build
```
После успешного запуска API будет доступно по адресу:
```
http://localhost:8000/
```

---

## Запуск без Docker (локально)
### **1. Установите Python 3.10 и создайте venv**
```sh
python -m venv .venv
```

### **2. Установите зависимости**
```sh
pip install -r requirements.txt
```

### **3. Создайте базу данных PostgreSQL**
Запустите PostgreSQL и создайте базу данных:
```sql
CREATE DATABASE sanicpay;
CREATE USER sanic WITH PASSWORD 'sanicpassword';
GRANT ALL PRIVILEGES ON DATABASE sanicpay TO sanic;
```

### **4. Настройте .env файл**
Создайте `.env.local` файл в корне проекта.
Просмотрите использование переменных в app/core/config.py !!!
```ini
HOST=0.0.0.0
PORT=8000
DEBUG=True
SECRET_KEY=private_key
DB_USER=sanic
DB_PASSWORD=sanicpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sanicpay
DATABASE_URL=postgresql+asyncpg://sanic:sanicpassword@localhost:5432/sanicpay
```

### **5. Выполните миграции базы данных**
```sh
alembic upgrade head
```

### **6. Запустите приложение**
```sh
python server.py
```
После успешного запуска API будет доступно по адресу:
```
http://localhost:8000/
```

---

## **Доступные тестовые пользователи**
### **Администратор**
- **Email:** `admin@example.com`
- **Пароль:** `adminpassword`

### **Обычный пользователь**
- **Email:** `testuser@example.com`
- **Пароль:** `testpassword`

---

## **Тестирование API**
После запуска API можно выполнить тестовые запросы. Примеры запросов в test_requests.py.
Пример аутентификации:
```python
import requests

url = "http://localhost:8000/api/v1/auth"
headers = {"Content-Type": "application/json"}

data = {
    "email": "testuser@example.com",
    "password": "testpassword"
}

response = requests.post(url, json=data, headers=headers)
print(response.text, response.status_code)
```

Полный список эндпоинтов доступен в коде проекта.

---
