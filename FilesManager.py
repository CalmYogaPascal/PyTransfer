import protos.Files_pb2 as Files
import protos.Files_pb2_grpc as FilesAuth
import protos.User_pb2 as Users


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
        channel: grpc.Channel
    ) -> None:
        self._channel = channel
        self._stub = FilesAuth.UserFileSystemInfoStub(self._channel)

    async def RequestFiles(self, login: str) -> None:
        request = Users.UserInfo(login=login)
        print("Request: %s" % (request))
        result = await self._stub.Request(request)
        print(result)

    event = asyncio.Event
    state_iterator = []

    async def StreamFilesRequest(self) -> None:
        logging.info("Nice")
        async def request_():
            onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]

            print(onlyfiles)
            t=Files.Directory()
            for k in onlyfiles:
                file = Files.File
                file.FileSize = os.path.getsize(k)
                file.LastDate = os.path.getmtime(k)
                file.Name = k
                t.FilePath.append(file)

            print(onlyfiles)
            print(t)
            yield t

            while True:
                await self.event.wait(self.event)
                self.event.clear(self.event)
                onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]

                t=Files.Directory()
                for k in onlyfiles:
                    #print(k)
                    t.FilePath.append(k)

                yield t

        self.state_iterator = self._stub.SendFileInfo(request_())

    async def StreamFilesReceive(self) -> None:
        async for response in self.state_iterator:
            self.event.set(self.event)
            logging.info(response)
        logging.warning("No streaming")