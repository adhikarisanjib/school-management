# **School Management Software**

## **A complete school management software that uses :<br>Esewa as payment gateway.<br>Agora as video conference tool.<br>Celery as backend task destribution.**

---

> ### **To run celery server**
>
> - celery -A school worker -l info

> ### **To dump and load test datas**
>
> - py manage.py dumpdata > db_data.json
>
> - py manage.py loaddata db_data.json
