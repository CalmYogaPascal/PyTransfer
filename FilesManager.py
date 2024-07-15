import typing
import protos.Files_pb2 as Files
import protos.Files_pb2_grpc as FilesAuth
import User_pb2 as Users


import grpc


import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isfile, join


class FilesManager:
    def __init__(
        self,
        channel
    ) -> None:
        self._channel = channel
        self._stub = FilesAuth.UserFileSystemInfoStub(channel)
        self.event = asyncio.Event()
        self.Quiting = False
        self._requests = typing.Set[Files.File]

    async def RequestFilesFromUser(self, login: str):
        request = Users.UserInfo(login=login)
        print("Request: %s" % (request))
        result = await self._stub.RequestFilesFromUser(request)
        print(result)
        return result

    async def StreamFiles(self):
        requests, responses = 0,0
        print("%s %s" % (requests, responses))
        async def ListDir():
            nonlocal requests, responses
            print("3: %s %s %s" % (requests, responses, not self.Quiting))
            while not self.Quiting:
                print("4: %s %s %s" % (requests, responses, not self.Quiting))
                while requests - responses >= 1:
                    await asyncio.sleep(1)
                files = [f for f in os.listdir() if os.path.isfile(f)]
                requests+=1
                dirr = Files.Directory()
                for file in files:
                    filesize = os.stat(os.path.abspath(file)).st_size
                    filemtime = os.stat(os.path.abspath(file)).st_mtime
                    DirectoryFile = dirr.files.add()
                    DirectoryFile.Name = file
                    DirectoryFile.FileSize = filesize
                    DirectoryFile.LastDate = int(filemtime)
                print("Files: %s" % (files))
                yield dirr

        print("1: %s %s" % (requests, responses))
        async for response in self._stub.StreamDirectory(ListDir()):
            print("2: %s %s" % (requests, responses))
            print(response)
            responses+=1
            await asyncio.sleep(1)