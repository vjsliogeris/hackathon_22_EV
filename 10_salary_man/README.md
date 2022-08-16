##Requirements:
* asgiref==3.5.2
* backports.zoneinfo==0.2.1
* Django==4.1
* lxml==4.9.1
* Pillow==9.2.0
* python-docx==0.8.11
* python-dotenv==0.20.0
* sqlparse==0.4.2
* translitcodec==0.7.0


Generate app password as noted [here](https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j)

put it in `salaryman/.env`.
as 
`APP_PW = PASSWORD`

open salaryman/main.py
Change `SENDER_EMAIL` as appropriate

##To run:
```bash
cd salaryman
python manage.py runserver
```
