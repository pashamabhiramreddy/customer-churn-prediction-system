FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile check to fail early on syntax/indentation errors
RUN python -m py_compile app.py

EXPOSE 5000

# Use Gunicorn for production WSGI serving
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]