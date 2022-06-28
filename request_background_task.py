# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 16:26
@Author: Jinpeng Yang
@Description: Background Tasks Tutorial
"""

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open('log.txt', 'w') as email_file:
        content = f'notification for {email}: {message}'
        email_file.write(content)


@app.post('/send-notification/{email}')
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {
        'msg': 'Notification sent in the background'
    }
