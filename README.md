## Installation Guidelines
### Clone repository to local computer
```
    git clone git@github.com:Aashish97/weather-app-backend.git
```

### Change directory to the project
```
    cd weather-app-backend
```

### Create and activate virtual environment
```
    python3 venv venv
    source venv/bin/activate
```

### Install project requirements
```
    pip install -r requirements.txt
```

### Migrate the existing database migrations
```
    python manage.py migrate
```
This should create a file named `db.sqlite3` which is the database to store the data for later purpose

### Feed the weather data to the database
```
    python manage.py feed_data_to_model
```
This may take 10-15 minutes depending upon the device. You can optimize this using pandas, numpy and iterable.

### After successfully migrating the data run the server
```
    python manage.py runserver
```
This should run on the localhost server on port 8000 http://127.0.0.1:8000

### See the weather data and weather stats data on the api
* http://127.0.0.1:8000/api/weather/ [Available filters: `station_id`, `data`]
* http://127.0.0.1:8000/api/weather/stats/ [Available filters: `station_id`, `year`]

### For API level documentation
* http://127.0.0.1:8000/swagger/

### Run test cases
```
    python manage.py test
```
Location of test weather_api>tests.py
