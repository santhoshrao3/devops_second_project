# Exam-Portal
This is an Exam Portal where a school can generate general knowledge quizes using Open Trivial DB API and students can login to take any quiz from any school.

# How to Run the Project on your Local?
1. Set up your python virtual environment
2. Fork and Pull or download the project on your local
3. Install the dependencies from requirements.txt using the following command \
  $ pip install -r requirements.txt
4. Run the following commands to migrate the Database and start the project on your localhost \
  $ python manage.py makemigrations \
  $ python manage.py migrate \
  $ python manage.py runserver \
5. Then you can login using schools to create new quizes and then login by student to attend the quiz. You can create multiple schools or student accounts.