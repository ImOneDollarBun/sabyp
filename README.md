## Платформа для быстрой презентации продукта
### Установка (```Linux``` & ```Windows```)
1. Клонирование и переход в директорию
```bash
git clone https://github.com/ImOneDollarBun/sabyp.git
cd sabyp
```
2. Создание виртуального окружения (на Linux нужен пакет ```python3.8-venv```)
```bash
python -m venv venv 
```
3. Активация виртуального окружения
######
На `Windows`
```bash
venv/Scripts/activate
```
На `Linux`
```bash
source venv/bin/activate
```
4. Установление зависимостей pip
```bash
pip install -r requirements.txt
```
5. Создание ключей безопасности JWT
```bash
python src/utils/certs/genkeys.py
```
6. Запуск приложения
####
С помощью python (стандартные настройки файла окружения ```.env```, порт `5000` хост `localhost`)
```bash
python main.py
```

С помощью uvicorn (кастом через флаги --host --port)
```bash
uvicorn main:app
```
---
Пример
```bash
uvicorn main:app --host 127.0.0.1 --port 34002
```
---
## Настройка
Основные файлы конфигурации `.env` и `config.py`. Файл окружения отвечает за основной порт приложения (default 5000) и учётные данные для базы данных PostgreSQL, стандартные настройки `.env`:
```text
#Fastapi
APP_PORT=5000

#Postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sabyp
```
