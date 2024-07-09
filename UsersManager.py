import logging
import protos.User_pb2 as Users
import protos.User_pb2_grpc as UsersAuth


import grpc
from google.protobuf.empty_pb2 import Empty


from typing import List


class UsersManager:
    def __init__(
        self,
        channel: grpc.Channel
    ) -> None:
        self._channel = channel
        self._stub = UsersAuth.UserAuthorizationStub(self._channel)

    async def connect(self) -> None:
        request = Empty()
        logging.info("Connecting: %s", request)
        return self._stub.Connect(request)

    async def disconnect(self) -> None:
        request = Empty()
        self.connect()
        await self._stub.Disconnect(request)

    async def get_users(self) -> List[str]:
        request = Empty()
        logging.info("%s" % (self._stub.GetUsers(request)))
        result: Users.UsersInfo = await self._stub.GetUsers(request)
        resultlist = []
        for k in result.users:
            resultlist.append(k.login)
        return resultlist