## Python web team project 'Jull assistant' <a><img src="https://github.com/DmytroSDV/Jull_web/blob/main/static/web_world.ico"></a>:
### Usage:
  - From the root folder where pyproject.toml exist run command:
    
        poetry install --no-root 
  - Run postgres and rediss docker containers with command:

        docker compose up -d
  - Make migrations by executing two commands from \app_jull\manage.py

        py manage.py makemigrations
    
        py manage.py migrate
  - Runserver from \hw10\ path:

        py manage.py runserver
  - Open one more termital window and from \app_jull\ folder run:

        celery -A app_jull worker -l info -P eventlet
  - Open one more termital window and from \app_jull\ folder run:

        celery -A app_jull beat -l info
  - Visit localhost:8000/

  - Optionally you can view how celery works, need to open one more terminal and from \app_jull\ folder run:

        celery -A app_jull flower --broker=redis://localhost:6379/0 --address='127.0.0.1' -l info --pool=eventlet
    and visit localhost:5555


### What Jull can do

   1. Save contacts with names, addresses, phone numbers, email and birthdays to the contact book;
   2. Display a list of contacts whose birthday is a specified number of days from the current date;
   3. Check the correctness of the entered phone number and email when creating or editing a record and notify the user in case of incorrect entry;
   4. Search for contacts among book contacts;
   5. Edit and delete entries from the contact book;
   6. Keep notes with text information;
   7. Search for notes;
   8. Edit and delete notes;
   9. Add "tags" to notes, keywords describing the topic and subject of the record;
   10. Search and sort notes by keywords (tags);
   11. Upload user files to the cloud service and have access to them. The user must be able to upload any file to the server through the web interface and download it;
   12. Sort user files by categories (images, documents, videos, etc.) and display only the selected category (file filter by category).
   13. Provide a brief summary of news for the day. Collect sports, sience, techno, article, usd currency, eur currency, weather information from the resources at the request of the user and display them on the results page. 
   14. Authentication
  - Implemented a user authorization mechanism. The web interface allowed access to its functions only to registered users;
  - Each registered user have access to their own data and files;
  - Implemented password recovery mechanisms for the user by email;

      poetry export -f requirements.txt --output requirements.txt --without-hashes
