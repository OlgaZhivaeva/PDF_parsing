## Создание и заполнение справочника на основе PDF документа

Используйте приложение для для создания и заполнения справочника на основе PDF документа
установленного техническим заданием образца
[Обзазец файла](https://drive.google.com/file/d/1ZW_gDdWLMkTcjz8jpleRCvhu9ArWWwlS/view)

### Как установить

Задайте путь к PDF документу на вашем компьютере в переменной `PDF` и все
необходимые значения переменных для подключения к базе данных postgres в 
файле `.env`

```
PDF="ххххххххххххххх"
LOGIN="хххххххх"
PASSWORD="хххххххх"
DATABASE="хххххххх"
HOST="хххххх"
PORT="ххххх"

```
Используйте Python3. Установите зависимости 

```
pip install -r requirements.txt
```
Запустите файл `main.py`
