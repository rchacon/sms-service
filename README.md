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

```
$ python scraper.py
```
