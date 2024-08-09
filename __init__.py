from concurrent.futures import ThreadPoolExecutor
import logging
import asyncio
import os
import time
import PySide6
import PySide6.QtAsyncio
        
import grpc.aio
import minio.credentials

from FilesManager import FilesManager
from MyWindow import MyWindow
import PySide6.Qt
from TransferManager import TransferManager
from UsersManager import UsersManager

import json
import minio

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import watchdog.events as Events
class FSMinioWatchDog(FileSystemEventHandler):
    def __init__(self, credentials):
        super().__init__()
        print(credentials["url"])
        self.client = minio.Minio(endpoint="127.0.0.1:9000",
                                  access_key=credentials["accessKey"],
                                  secret_key=credentials["secretKey"],
                                  secure=False)
        
        print(credentials["url"])
        self.bucket_name = "backup"
        
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)
            print("Created bucket", self.bucket_name)
        else:
            print("Bucket", self.bucket_name, "already exists")

            
    def on_any_event(self, event):
        if event.is_directory or event.event_type=="opened":
            return None
    
        
        elif event.event_type == 'created' or event.event_type=="modified":
            src_path = event.src_path
            if event.dest_path:
                src_path = event.dest_path
            dest_path = os.path.relpath(os.path.abspath(src_path),os.path.curdir)
            print(src_path, dest_path)
            result = self.client.fput_object(
                self.bucket_name, dest_path, src_path,
            )
            

            

def minio_watchdog(credentials):
    observer = Observer()
    handler = FSMinioWatchDog(credentials)
    observer.schedule(handler, path=os.path.curdir,recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    finally:
        observer.stop()
        observer.join()


async def run():
    print("Running")
    f_credentials = open("credentials.json")
    credentials = json.loads(f_credentials.read()) 
    print(credentials["url"], type(credentials))
    executor = ThreadPoolExecutor(max_workers=1)
    wd_future = executor.submit(minio_watchdog, credentials)
    f_credentials.close()
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        logging.info("Waiting for channel to be ready")
        await channel.channel_ready()
        
        logging.info("Setting up rpc managers")
        users = UsersManager(channel=channel)
        files = FilesManager(channel=channel)
        transfer = TransferManager(channel=channel)
        

        logging.info("Setting up GUI")
        w = MyWindow(users, files, transfer)
        w.show()

        logging.info("Running")
        while not files.Quiting:
            await asyncio.sleep(1)
        
        await users.disconnect()
    executor.shutdown(cancel_futures=True)

    
        
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    app = PySide6.QtWidgets.QApplication(sys.argv)
    
    PySide6.QtAsyncio.run(run())
    
    