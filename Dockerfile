FROM python:3.8

#RUN mkdir ./app
WORKDIR /app
COPY . /app/


RUN pip install virtualenv 
ENV PATH="/app/env/bin:$PATH"
RUN pip install -r requirements.txt --no-cache-dir



EXPOSE 8000
CMD ["bash","-c","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

