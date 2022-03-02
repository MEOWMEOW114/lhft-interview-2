## installation

➜ backend python3.9 -m venv venv

➜ backend source venv/bin/activate
(venv) ➜ backend python --version
Python 3.9.1

pip install fastapi "uvicorn[standard]"

## how to run

source venv/bin/activate
uvicorn run:app --reload

## how to kill

lsof -i:8000
kill 52738
