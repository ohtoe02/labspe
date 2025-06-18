FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/www/html/frontend /var/www/html/backend

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 