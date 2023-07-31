# Aeon API

API for [Aeon Bot](https://github.com/renaism/aeon-bot).

## Requirements
- Python >3.10
- MongoDB >6.0.7

## Usage
- Clone the repository
```bash
git clone https://github.com/renaism/aeon-api.git &&\
cd aeon-api
```

- Create and activate python virtual environment
```bash
python -m venv venv &&\
source venv/bin/activate
```

- Install requirements
```bash
pip install -r requirements.txt
```

- Configure environment variables
```bash
touch .env
```

```
# .env

# Insert your API key secret here
API_KEY_SECRET=XXX

# Insert the database credentials here
DB_HOST=127.0.0.1:27017
DB_NAME=dbname
DB_USERNAME=username
DB_PASSWORD=xxx
```

- Start the API
```bash
python main.py
```