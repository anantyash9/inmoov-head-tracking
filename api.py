from fastapi import BackgroundTasks, FastAPI
from time import sleep
import uvicorn
app = FastAPI()


def write_notification():
    while True:
        print("running!")
        sleep(2)

@app.post("/start")
async def start_cam(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification)
    return {"message": "Notification sent in the background"}

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=5000)