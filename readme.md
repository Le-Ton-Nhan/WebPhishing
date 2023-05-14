Setting: 
python -m venv model
cd model
cd Scripts
activate
cd ..
cd ..
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
django-admin startproject detect_phishing_link
cd detect_phishing_link
django-admin startapp phishing
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

#tạo user admin
py manage.py createsuperuser 
admin
admin

