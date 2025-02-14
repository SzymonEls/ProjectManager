FROM python:3.12.3
ADD . /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
#RUN apt-get update && apt-get install -y certbot openssl
RUN chmod +x ./start.sh
CMD ["/bin/bash", "./start.sh"]
EXPOSE 443