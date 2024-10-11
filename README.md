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
   # Информация выводящаяся в блоке "О нас", координаты для яндекс карты
  {
    "name": "about",
    "value": "Мы занимаемся лесом уже на протяжении более чем 12 лет. Делаем это хорошо!",
    "additional": {
      "phone": "89830510328",
      "email": "nikishev.dev@gmail.com",
      "map": [
        56.530672,
        85.058995
      ]
    },
    "uuid": "ff7123ca-ce76-40b7-b46b-d70c30c9726e"
  }
```