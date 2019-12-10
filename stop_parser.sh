docker exec abb_mariadb mysql -uscrapper -p123456 allbestbets --init-command="update work_parser set status=4, status_work='parser was stoped...';"
echo 'stoping mariadb on docker container...please wait for 10s'
sleep 10s
docker stop abb_mariadb
docker rm abb_mariadb
