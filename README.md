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