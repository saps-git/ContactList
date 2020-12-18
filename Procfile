release: python manage.py makemigrations --no-input 
release: python manage.py migrate --no-input

web: gunicorn contactsapi.wsgi 

//release contains commands that are to be executed on every run in the main server
// web is from where the applcation should be exectuted, on gunicorn server, contactsapi.wsgi(local serevr)