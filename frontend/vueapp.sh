docker run \
-p 3000:80 \
-d --name vuenginxnew \
--mount type=bind,source=$HOME/SelfWork/docker/vueclidemo/nginx,target=/etc/nginx/conf.d \
--mount type=bind,source=$HOME/SelfWork/docker/vueclidemo/dist,target=/usr/share/nginx/html \
nginx
