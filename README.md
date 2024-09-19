# Create a new Django project
    django-admin startproject <project_name>
# Run the server
    python manage.py runserver
# Create a new app
    django-admin startapp <app_name>


# Create a new migration
    python manage.py makemigrations
# Apply the migrations
    python manage.py migrate
# Create a superuser
    python manage.py createsuperuser


# Check dependencies
    pip freeze
# Create requirements.txt
    pip freeze > requirements.txt
# Install dependencies
    pip install -r requirements.txt