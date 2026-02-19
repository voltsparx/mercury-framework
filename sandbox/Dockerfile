FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MERCURY_SAFE=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN useradd --create-home --uid 10001 mercury && chown -R mercury:mercury /app
USER mercury

# Example sandbox image for safe local plugin simulation.
CMD ["python", "-c", "print('Mercury sandbox image ready')"]
