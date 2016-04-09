SMS service built on top of Google Voice


## Installation

```
$ pip install -r requirements.txt
```

Add google credentials to `.gvoice`

The scraper uses the environment variable `MONGO_URI` for connecting to mongo.

```
$ export MONGO_URI=<MONGO_URI>
```

If not set, the following URI will be used: `mongodb://localhost:27017/sms`.

## Usage

Run Scraper

```
$ python scraper.py
```

Run Web application in development mode

```
$ python app.py
```

Run Web application in production mode

```
$ gunicorn app:app --workers=4
```

REST API Documentation

GET `/api/sms?phone=(510)%20555-5555`

```
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
