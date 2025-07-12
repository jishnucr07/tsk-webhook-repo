# use python image

FROM python:3.9.23

#working dir
WORKDIR /app

#copy requirements.txt 
COPY requirements.txt .

#install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copying all the other files
COPY . .

#Exposing the port
EXPOSE 5000

#Run the app

CMD ["python","run.py"]