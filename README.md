# Vortex-app
A simple web service for Food recipes.

# Instalation
## With Docker
Run the following commands:
docker build -t “foodrecipe.com:Dockerfile”
docker-compose up --build

## Without Docker
Run the following commands:
python -m venv venv
source .venv/bin/activate or .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# APIs
List of available API can be found on http://localhost:8000/api/docs

# Testing

To run unittests, run the following command:
python manage.py test
