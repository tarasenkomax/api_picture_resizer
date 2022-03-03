### Задание

https://documenter.getpostman.com/view/2157092/TzkzrzNU

Необходимо разработать сервис, на основе фреймворка Django c использованием DRF, который позволит загружать изображения
с компьютера пользователя, или по ссылке, а затем изменять их размер используя библиотеку Pillow. Изображения должны
сохраняться на диск. Так же необходимо реализовать api в соответствии с запросами в POSTMAN (ссылка выше).

### Необходимое окружение

* Python 3.7

### Документация

https://docs.google.com/document/d/1Gen-3wN5TXiwdS-p3p19vLgBGc6sbqMRnrUI4rzfd_g/

### Развертывание

1. Скачать с репозитория
2. Установить виратульное окружение Python  
   `python3.7 -m venv venv`
4. Активировать виртуальное окружение  
   `source venv/bin/activate`
5. Установить зависимости  
   `pip install -r requirements.txt`
6. Выполнить миграции  
   `python manage.py migrate`
7. Создать суперпользователя для доступа к панели администратора  
   `python manage.py createsuperuser`
8. Запустить приложение  
   `python manage.py runserver`