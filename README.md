SMS service built on top of Google Voice


## Installation

```
$ pip install -r requirements.txt
```

`pygooglevoice` creates a `.gvoice` in your home directory where you add your google credentials.

The scraper and web application use the environment variable `MONGO_URI` for connecting to mongo.

```
$ export MONGO_URI=<MONGO_URI>
```

If not set, the following URI will be used: `mongodb://localhost:27017/sms`.

You are also going to need RabbitMQ

## Usage

Run Scraper

```
$ python scraper.py
```

Run rabbitmq workers

```
$ python worker.py
```

Run Web application in development mode

```
$ python app.py
```

Run Web application in production mode


```
$ gunicorn app:app --workers=4
```

## REST API Documentation

Get all text messages exchanged with some phone number.

GET `/api/sms?phone=(510)%20555-5555`

```
curl 'localhost:5000/api/sms?phone=(510)%20555-5555'
```

```json
{
  "count": 2,
  "results": [
    {
      "conversation_id": "c86adf423883774c4f5b326467874c1e9b99a5ec",
      "from": "Hank Hill:",
      "phone": "(510) 555-5555",
      "text": "I tell ya what",
      "time": "8:39 AM"
    },
    {
      "conversation_id": "c86adf423883774c4f5b326467874c1e9b99a5ec",
      "from": "Me:",
      "phone": "(510) 555-5555",
      "text": "That boy ain't right",
      "time": "8:41 AM"
    }
  ]
}
```

Send a text message.

POST `/api/sms`

```
curl -H "Content-Type: application/json" -X POST -d '{"message": "it works?", "phone": "5105555555"}' http://localhost:5000/api/sms
```

```json
{
  "status": "success"
}
```

## Running Tests

```
$ pip install nose==1.3.7
```

```
$ nosetests
```
