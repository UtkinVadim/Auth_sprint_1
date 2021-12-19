FROM python:3.9.7-slim
WORKDIR /functional

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG USER=auth_api_user
RUN addgroup --system ${USER} && \
    adduser --system --no-create-home --ingroup ${USER} ${USER} && \
    chown -R ${USER}:${USER} /app
USER $USER

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENTRYPOINT ["/bin/sh", "-c", "wait_for_postgres.sh"]
CMD [""]
