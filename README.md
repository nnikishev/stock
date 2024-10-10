 # Settings application for FE app
 ## Installation for linux
 ```
 python3 -m venv .venv
 source .venv/bin/activate
 pip3 install -r requirements.txt
 ```
 ## Making migrations
 ```
 (.venv) nikolay@nikolay-BOD-WXX9:~/projects/information_security/businnes_app$ alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'settings'
  Generating /home/nikolay/projects/information_security/businnes_app/alembic/versions/09083158c38e_.py ...  done
(.venv) nikolay@nikolay-BOD-WXX9:~/projects/information_security/businnes_app$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 97ce5434472c -> 09083158c38e, empty message
(.venv) nikolay@nikolay-BOD-WXX9:~/projects/information_security/businnes_app$ 
```
 ## Start application
 ```
 uvicorn main:app --reload
 ```

 ## System settings:
 ```
  # Заголовок используюшийся в приложении
 {
    "name": "title",
    "value": "ЛесСтройТорг",
    "additional": null,
    "uuid": "3f5db04d-8016-4974-8694-08393bad8861"
  }
   # Информация выводящаяся в блоке "О нас"
  {
    "name": "about",
    "value": "Мы занимаемся лесом ужа на протяжении более чем 12 лет. Делаем это хорошо!",
    "additional": {
      "phone": "89830510328",
      "email": "nikishev.dev@gmail.com"
    },
    "uuid": "ff7123ca-ce76-40b7-b46b-d70c30c9726e"
  }
   # Информация выводящаяся в блоке "Почему мы?"
  {
    "name": "why_us",
    "value": "",
    "additional": {
      "1": "Молодое, активно развивающееся производство, объем производства вырос в 7 раз за 3 года.",
      "2": "Постоянная модернизация оборудования.",
      "3": "27 городов рф и 3 страны присутствия.",
      "4": "Основные породы сосна и кедр.",
      "5": "Безотходное производство, отходы перерабатываются в пелеты.",
      "6": "На 26 год запланирован запуск производства на новой площадке"
    },
    "uuid": "ae189c08-45fd-4f85-95a1-9fdf1dc309db"
  }
```