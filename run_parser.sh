docker exec abb_mariadb mysql -uscrapper -p123456 allbestbets --init-command="update work_parser set status=1;"
. env/bin/activate
env/bin/python3 script.py
