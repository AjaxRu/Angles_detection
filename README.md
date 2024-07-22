# Angles detection 
Клонируйте репозиторий себе в папку: <br/>
`git clone https://github.com/AjaxRu/angles_detection.git` <br/>
`cd angles_detection`
## ЗАПУСК 
`docker-compose up --build` 
## ТЕСТЫ 
Для прохождения тестов откройте новое окно, перейдите в папку проекта и выполните:
### 1. Литинг кода
`docker-compose exec web flake8 .` <br/>
![image](https://github.com/user-attachments/assets/0a11c1de-5c78-4d8e-b29b-4e703c4795cf)
### 2. Анализ кода с помощью radon
`docker-compose exec web radon mi -s -i venv .` <br/>
![image](https://github.com/user-attachments/assets/aac2b874-5091-4206-9c56-6f6bf73ad968)
`docker-compose exec web radon cc -s -i venv .` <br/>
![image](https://github.com/user-attachments/assets/d33743e9-385d-4de4-88f0-bbbb8179847f)
### 3. Проверка безопасности кода с помощью bandit
`docker-compose exec web coverage html` <br/>
![image](https://github.com/user-attachments/assets/310346e8-8bcc-4028-bf8b-b3a18e6870a0)
### 4. Покрытие тестов
`docker-compose exec web coverage run --rcfile=.coveragerc manage.py test` <br/>
`docker-compose exec web coverage report` <br/>
![image](https://github.com/user-attachments/assets/09806172-24b7-44c2-8363-d707907350bf)
## РАБОТА С КОЛЛЕКЦИЕЙ В POSTMAN
### Выполните
`docker-compose exec web python manage.py migrate` <br/>
Создайте суперпользователя <br/>
`docker-compose exec web python manage.py createsuperuser` <br/>
### Откройте коллекцию angle_detection.postman_collection.json в Postman
Для получения токена используйте запрос Token_obtain с введенными данными суперпользователя <br/>
![image](https://github.com/user-attachments/assets/f77abef2-9113-4f83-a18c-a968fb16db37)
Для обновления токена используйте запрос Token Refresh и введите "refresh" из предыдущего запроса <br/>
Для получения точек интереса с изображения используйте запрос Image Detection, в окне авторизации вставьте "access" из запроса по получению токена, и вставьте в "image" желаемое изображение, например test_image.jpg <br/>
![image](https://github.com/user-attachments/assets/16bafcdf-48f3-450b-8a14-798d7256419b)
Пример найденных точек интереса, отмеченных на оригинальном изображении: <br/>
![image](https://github.com/user-attachments/assets/5b668e22-7e1c-484c-a8c5-86d753e02c6b)



