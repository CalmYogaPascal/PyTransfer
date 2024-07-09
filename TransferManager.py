import logging
import protos.User_pb2 as Users
import protos.Transfer_pb2 as Transfer
import protos.Transfer_pb2_grpc as TransferAuth


import grpc
from google.protobuf.empty_pb2 import Empty


from typing import List


class TransferManager:
    def __init__(
        self,
        channel: grpc.Channel
    ) -> None:
        self._channel = channel
        self._stub = TransferAuth.FileTransferStub(self._channel)

    async def connect(self) -> None:
        request = Empty()
        logging.info("Connecting: %s", request)
        return self._stub.FileTransferListener(request)
        logging.info("Connected")

    async def disconnect(self) -> None:
        request = Empty()
        self._stub.Disconnect(request)

    async def get_users(self) -> List[str]:
        request = Empty()
        result: Users.UsersInfo = self._stub.GetUsers(request)
        resultlist = []
        print(type(result))
        print(result)
        for k in result.users:
            resultlist.append(k.login)
        return resultlist