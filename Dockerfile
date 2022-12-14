# start by pulling the python image
FROM python:3

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . .

CMD ["waitress-serve", "server:app"]

EXPOSE 8080