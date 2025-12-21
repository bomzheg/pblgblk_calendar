# pblgblk_calendar
[![wakatime](https://wakatime.com/badge/user/929ee39b-4eb0-4076-ab5e-5ade3c56e464/project/a7990aa9-785d-4993-baaf-369ee65f80bf.svg)](https://wakatime.com/badge/user/929ee39b-4eb0-4076-ab5e-5ade3c56e464/project/a7990aa9-785d-4993-baaf-369ee65f80bf)

## How to run

Required launched PostgreSQL and installed Python3.10

* copy config template
```bash
cp -r config_dist config
```
* Fill config/config.yml in with required values 
* Create and activate venv
```bash
python -m venv venv
source venv/bin/activate
```
* install dependencies
```bash
pip install -r requirements.txt
```
* Fill in alembic.ini (probably only db url)
* apply migrations
```bash
alembic upgrade head
```
* ... and run
```bash
python -m app
```
