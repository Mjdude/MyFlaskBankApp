echo "Starting Flask App..."
gunicorn -b 0.0.0.0:8000 app:app
