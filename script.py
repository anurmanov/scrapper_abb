import asyncio
from allbestbets import parser as abb
#from bet_company1 import parser as bt1
#from bet_company2 import parser as bt2

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(abb.parse_periodic()),]
    #using asynchronous code we can 'concurrently' run multiple parsers of the different bet companies
    #tasks = [loop.create_task(abb.parse_periodic()), loop.create_task(bt1.parse_periodic()), loop.create_task(bt2.parse_periodic()),]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
