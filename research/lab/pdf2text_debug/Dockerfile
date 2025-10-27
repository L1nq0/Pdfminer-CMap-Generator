# Use official Python image
FROM python:3.10-slim-bullseye

COPY ./app /app
COPY ./start.sh /

# Create app user
RUN useradd -m app && \
    chown -R app:app /app &&\
    mkdir -p /app/uploads && chown -R app:app /app/uploads && chmod 755 /app/uploads &&\
    touch /flag && chown app:app /flag

# Set working directory
WORKDIR /app

RUN pip install --no-cache-dir -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt

USER app

# Expose port
EXPOSE 5000

# Run application
CMD ["/bin/bash", "/start.sh"]