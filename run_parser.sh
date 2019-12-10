docker run -p 3306:3306 --name abb_mariadb -v $(pwd)/docker/allbestbets/data:/var/lib/mysql -v $(pwd)/docker/allbestbets/my.cnf:/etc/mysql/my.cnf -v $(pwd)/docker/allbestbets/init-db:/docker-entrypoint-initdb.d -e MYSQL_ROOT_PASSWORD=prosto_mariadb mariadb:10.4-bionic 1>>/dev/null 2>>/dev/null &
echo 'starting mariadb on docker container...please wait for 10s'
sleep 10s
docker exec abb_mariadb mysql -uscrapper -p123456 allbestbets --init-command="update work_parser set status=1, status_work='parser was started...';"
. env/bin/activate
env/bin/python3 script.py
