FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY /keys/fullchain.pem /etc/ssl/certs
COPY /keys/privkey.pem /etc/ssl/certs
COPY proxy.conf /etc/nginx/conf.d
