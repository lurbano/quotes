import asyncio
from aiohttp import web, ClientSession
from datetime import datetime
import json
#from getIP import getIP
from uAio import *

# database
from quotesDB import *
db = quotesDB()

dir_path = os.path.dirname(os.path.abspath(__file__))

async def handle(request):
    with open(dir_path+"/"+"index.html", "r") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

async def handleAdd(request):
    with open(dir_path+"/"+"add.html", "r") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

async def handleEdit(request):
    with open(dir_path+"/"+"edit.html", "r") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')


async def handlePost(request):
    data = await request.json()
    rData = {}
    print(data)
    # print(data["action"], data["value"])

    if data['action'] == "getTime":
        now = datetime.now()
        print(now.ctime())
        rData['item'] = "time"
        rData['status'] = now.ctime() # a string representing the current time

    if data['action'] == 'addQuote':
        info = data['value']
        print("Adding: ", info)
        q_id = db.insert(
            username=info['username'], 
            quote=info['quote'], 
            quoteAuthor=info['quoteAuthor'],
            quoteDate=info['quoteDate'],
            quoteSource=info['quoteSource'] 
        )
        rData['item'] = 'addQuote'
        rData['status'] = f"added {info['quoteAuthor']} ({q_id})"

    if data['action'] == 'getRandomQuote':
        info = data['value']
        print("Getting: ", info)

        rData['item'] = 'quote'
        rData['status'] = db.getRandom()
    
    if data['action'] == 'markAsRead':
        id = data['value']
        print("Getting id: ", id)

        rData['item'] = 'markAsRead'
        rData['status'] = 'marked'
    

    

    response = json.dumps(rData)
    print("Response: ", response)
    return web.Response(text=response, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/add', handleAdd)
    app.router.add_get('/edit', handleEdit)
    app.router.add_post("/", handlePost)

    # Serve static files from the "static" directory
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    app.router.add_static('/static/', path=static_path, name='static')
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = 14142

    host = getIP()
    site = web.TCPSite(runner, host, port)  # Bind to the local IP address
    await site.start()
    print(f"Server running at http://{host}:{port}/")

    # asyncio.create_task(print_hello())
    # asyncio.create_task(getLightLevel(dt=5))

    '''Testing post request'''
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")

    await asyncio.Event().wait()  # Keep the event loop running

if __name__ == '__main__':
    asyncio.run(main())