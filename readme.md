## Active Virtual Environment
```bash 
python -m venv venv
venv/Scripts/activate
```

## Install requirements
```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Start django-admin
```bash 
django-admin startproject detect_phishing_link
cd detect_phishing_link
django-admin startapp phishing
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


## Create user
```bash
py manage.py createsuperuser 
```
> username: admin
>
> password: admin
