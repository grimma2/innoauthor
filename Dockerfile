# Используем официальный базовый образ Python 3.10
FROM python:3.10-slim

# Устанавливаем переменную окружения для предотвращения буферизации вывода Python
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости, указанные в requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . /app/

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда запуска сервера разработки Django
CMD ["python", "manage.py", "runserver"]
