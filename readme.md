# Source initialization 

| One time initialization 

## Init project django-admin
```bash 
django-admin startproject detect_phishing_link
cd detect_phishing_link
django-admin startapp phishing
```

## Create user
```bash
py manage.py createsuperuser 
```

| username | password | 
|----------|----------|
| admin    | admin    |

# Runtime

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

## Start project
```bash
python manage.py runserver
```

