FROM python:3.13.3-alpine3.20
WORKDIR /app

# Установка зависимостей и очистка кеша
RUN apk add --no-cache gcc musl-dev postgresql-dev chromium chromium-chromedriver && \
    pip install --upgrade pip && \
    rm -rf /var/cache/apk/*

# Копирование файлов проекта
COPY . /app

# Установка Python-зависимостей
RUN pip install -r requirements.txt

CMD ["python", "main_selenium.py"]