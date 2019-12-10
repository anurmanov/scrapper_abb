docker exec abb_mariadb mysql -uscrapper -p123456 allbestbets --init-command="update work_parser set status=4, status_work='parser was stoped...';"
