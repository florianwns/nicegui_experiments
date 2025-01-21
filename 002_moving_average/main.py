#!/usr/bin/env python3
"""An app who take a video then generate secondary images.
"""
import base64
import threading
from datetime import datetime
from typing import Union

import aiofiles
import cv2
from nicegui import ui, events


def log(message: Union[str, Exception]):
    date_str = datetime.now().strftime('%X.%f')[:-5]
    log_element.push(
        f"{date_str} | {message}"
    )


def on_frame(index: int, frame: cv2.typing.MatLike) -> None:
    print(index, frame.shape)


def decode_video(filepath, notify, container):
    try:
        stream = cv2.VideoCapture(filepath)
        if not stream.isOpened():
            raise Exception("cv2: Video stream can't be opened")

        frame_index = 0
        avg_image = None
        while True:
            frame_got, frame = stream.read()
            if frame_got:
                frame_index += 1
                on_frame(frame_index, frame)
                notify(f"{frame_index} | {frame.shape}")
                if frame_index > 100:
                    break
                if avg_image is None:
                    avg_image = frame.astype('float32')
                else:
                    avg_image + frame

        _, buffer = cv2.imencode('.jpeg', avg_image.astype('uint8'))
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        with container:
            ui.image(f"data:image/jpeg;base64,{encoded_image}")


    finally:
        if stream and stream.isOpened():
            notify("cv2: Release video stream")
            stream.release()


async def handle_upload(args: events.UploadEventArguments) -> None:
    try:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
            contents = args.content.read()
            await temp_file.write(contents)

            filepath = temp_file.name
            log(f"Start to decode {filepath}")
            threading.Thread(
                target=decode_video,
                args=(filepath, log, container)
            ).start()

    except Exception as e:
        log(e)


with ui.card().classes("absolute-center w-[860px] p-10") as container:
    upload_input = ui.upload(
        label='Upload a video file',
        auto_upload=True,
        on_upload=handle_upload
    ).classes('w-full')
    log_element = ui.log(max_lines=10).classes('w-full h-40')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        port=8093,
        storage_secret='THIS_NEEDS_TO_BE_CHANGED'
    )
