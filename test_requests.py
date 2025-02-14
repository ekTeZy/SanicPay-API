"""
Этот файл содержит набор тестовых HTTP-запросов к API SanicPay.

Инструкция по использованию:
Сначала выполните **аутентификацию (auth)**, чтобы получить `api_token` и `id` пользователя.
   - Вставьте полученный `api_token` в заголовки последующих запросов.
   - Запишите `id` пользователя, чтобы использовать его в других запросах.

Используйте другие запросы:
   - Получение информации о пользователе (`/users/{user_id}`)
   - Получение списка счетов (`/accounts`)
   - Пополнение баланса через вебхук (`/webhook`)
   - Удаление пользователя (`/users/{user_id}`) — доступно только для админа.
   - И так далее...

Примечания:
- **Токены в коде** (test user / admin) актуальны только после создания тестовых данных.
- **Порядок выполнения запросов важен**, сначала `auth`, затем остальные.
- Для каждого запроса указывайте **корректный токен аутентификации**.

🛠 Для запуска тестов просто раскомментируйте нужный блок кода.
"""



# import requests

# url = "http://localhost:8000/api/v1/auth"
# headers = {
#     "Content-Type": "application/json"
# }

# data = {
#     "email": "testuser@example.com",
#     "password": "testpassword",
# }

# try:
#     response = requests.post(url=url, json=data, headers=headers)
#     print(response.text, response.status_code)
# except Exception as e:
#     print(str(e))


# url = "http://localhost:8000/api/v1/users/2"  
# headers = {
#     "Authorization": "Token 639ae9fbd847eb2754d61872b41ecf6e85e1d0aa617b47269ff1868ff878bb34",
#     "Content-Type": "application/json"
# }

# try:
#     response = requests.get(url=url, headers=headers)
#     print(response.text, response.status_code)
# except Exception as e:
#     print(str(e))


# url = "http://localhost:8000/api/v1/accounts"
# headers = {
#     "Authorization": "Token a8dcd1911822e2219fb6f8359650730bdcd7a87568f0b494ad9c3fdeb62aba55",
#     "Content-Type": "application/json"
# }

# try:
#     response = requests.get(url=url, headers=headers)
#     print(response.text, response.status_code)
# except Exception as e:
#     print(str(e))
    

# url = "http://localhost:8000/api/v1/webhook"
# headers = {
#     "Content-Type": "application/json"
# }

# data = {
#     "transaction_id": "txn_123456",
#     "user_id": 2,
#     "account_id": 1,
#     "amount": 50.0,
#     "signature": "test_signature",
# }

# try:
#     response = requests.post(url=url, json=data, headers=headers)
#     print(response.text, response.status_code)
# except Exception as e:
#     print(str(e))

# url = "http://localhost:8000/api/v1/users/2"
# headers = {
#     "Authorization": "Token a8dcd1911822e2219fb6f8359650730bdcd7a87568f0b494ad9c3fdeb62aba55",
#     "Content-Type": "application/json"
# }

# try:
#     response = requests.delete(url=url, headers=headers)
#     print(response.text, response.status_code)
# except Exception as e:
#     print(str(e))
