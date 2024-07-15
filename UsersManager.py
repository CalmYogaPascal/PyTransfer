import logging
import User_pb2 as Users
import protos.User_pb2_grpc as UsersAuth


import grpc
from google.protobuf.empty_pb2 import Empty


from typing import List


class UsersManager:
    def __init__(
        self,
        channel
    ) -> None:
        self._channel = channel
        self._stub = UsersAuth.UserAuthorizationStub(self._channel)

    async def connect(self) -> None:
        request = Empty()
        logging.info("Connecting.")
        await self._stub.Connect(request)
        logging.info("Connected.")

    async def disconnect(self) -> None:
        request = Empty()
        logging.info("Disconnecting.")
        await self._stub.Disconnect(request)
        logging.info("Disconnected.")

    async def get_users(self) -> List[str]:
        request = Empty()
        result: Users.UsersInfo = await self._stub.GetUsers(request)
        resultlist = list()
        for k in result.users:
            resultlist.append(k.login)
        return resultlist