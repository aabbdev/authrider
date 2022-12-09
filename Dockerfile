FROM python:3.9-alpine AS build-env
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --disable-pip-version-check --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3
WORKDIR /app
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
ENV ENVIRONMENT="production"
ENV PYTHONUNBUFFERED=1
EXPOSE 3000

CMD ["wsgi.py"]