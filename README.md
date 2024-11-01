# Server

Lyra's default server for SLMs

### Virtual envs

STAGE means "build" or "dev", remove also the "[]"

For GNU/Linux we use

```
python -m venv env

source env/bin/activate

pip install -r ./[STAGE]-requirements.txt
```

For windows we use

```
python -m venv env

.\env\Scripts\activate

pip install -r ./[STAGE]-requirements.txt
```
