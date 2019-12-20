docker run \
-p 5000:5000 \
-d --name flaskserver \
--link chrome:chrome \
flaskwebserver
