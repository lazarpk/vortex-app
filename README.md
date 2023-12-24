# Vortex-app
A simple web service for Food recipes.

# Instalation
## With Docker
Run the following commands: <br/>
docker build -t “foodrecipe.com:Dockerfile” <br/>
docker-compose up --build

## Without Docker
Run the following commands: <br/>
python -m venv venv <br/>
source .venv/bin/activate or .\venv\Scripts\activate <br/>
pip install -r requirements.txt <br/>
python manage.py makemigrations <br/>
python manage.py migrate <br/>
python manage.py runserver <br/>

# APIs
List of available API can be found on http://localhost:8000/api/docs

# Testing

To run unittests, run the following command: <br/>
python manage.py test
