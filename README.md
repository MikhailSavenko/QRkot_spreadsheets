# QRkot_spreadsheets

**QRkot_spreadsheets** — это учебный проект, основанный на фонде помощи котам **cat_charity_fund**. В этом проекте добавлена возможность формирования отчётов в Google Sheets с использованием Google API.

## Клонирование репозитория

```bash
git clone git@github.com:MikhailSavenko/QRkot_spreadsheets.git
cd cat_charity_fund
```

## Установка зависимостей

### 1. Создайте и активируйте виртуальное окружение:

#### Для Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### Для macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

Добавьте ваши данные для подключения к Google API в файл `.env` или в переменные окружения. Пример значений:

```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SLOVO

TYPE=service_account
PROJECT_ID=<ваш_project_id>
PRIVATE_KEY_ID=<ваш_private_key_id>
PRIVATE_KEY=<ваш_private_key>
CLIENT_EMAIL=<ваш_client_email>
CLIENT_ID=<ваш_client_id>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=<ваш_client_x509_cert_url>
EMAIL=<ваш_email>
```

### Где взять данные для Google API:

1. Создайте новый проект в [Google Cloud Console](https://console.cloud.google.com/).
2. Включите Google Sheets API.
3. Создайте учетные данные типа `Service Account` и скачайте файл с учетными данными.
4. Из файла с учетными данными добавьте значения в соответствующие переменные в `.env`.

## Запуск приложения

После настройки переменных окружения и установки всех зависимостей, вы можете запустить приложение с помощью **Uvicorn**:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Возможности проекта

- Формирование отчётов по пожертвованиям и проектам фонда в Google Sheets.
- Работа с Google API через сервисный аккаунт.