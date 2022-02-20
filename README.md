# lib_book_tracking
Book Tracking Application across the multiple libraries.

## Steps to run this project.
**1. First Clone this repo into your local system.**

```bash
git clone https://github.com/NiteshTyagi/lib_book_tracking.git
```

**2. Then after cloning, open terminal and navigate to the lib_book_tracking folder into local system.**

**3. Install the required python library which needs to run this application properly.**

```bash
pip install -r requirements.txt
```

**4. Then Run the following commands:**

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

**5. Create a superuser to login into django-admin panel (/admin)**

```bash
python3 manage.py createsuperuser
```

**6. Last step: Run the Django server on 8080 because this port is used in test cases**

```bash
python3 manage.py runserver 0:8080
```

**7. To execute the test cases run the below command.**

```bash
python3 manage.py test
```

**8. If everything works as expected, then Open the browser and run the localhost:8080/admin URL or go to lib_book_tracking/urls.py for URL references.**