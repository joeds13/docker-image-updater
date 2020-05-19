FROM python:3.7-alpine

COPY python ./

RUN pip install --trusted-host pypi.org --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "updater.py"]
