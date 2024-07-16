import asyncio
import logging
import os
import typing

import grpc
import protos.Transfer_pb2 as Transfer
import protos.Transfer_pb2_grpc as TransferAuth

from google.protobuf.empty_pb2 import Empty

class TransferManager:
    def __init__(
        self,
        channel
    ) -> None:
        self._channel = channel
        self._stub = TransferAuth.FileTransferStub(self._channel)
        self.Quiting = False
        self.Transfers: typing.List[Transfer.FileTransferRequestInit] = []
    
    async def FileTransferProcessUpload(self):
        logging.info("Upload initiated")
        
        async def ReadFile():
            while not self.Quiting:
                while self.Transfers.__len__() == 0:
                    await asyncio.sleep(1)
                
                print("File to read: ",self.Transfers.__len__())
                transfer = self.Transfers.pop(0)
                offset = 0
                srcfile = os.path.abspath(transfer.SrcFile.Name)
                f = open(srcfile, "rb")
                
                filesize = os.path.getsize(srcfile)
                print("File to read1: %s %s %s %s" % (transfer,offset,srcfile,filesize))
                while offset < filesize:
                    result = Transfer.FilePartInfo()
                    f.seek(offset, 0)
                    buffersize = min(65536, filesize-offset)
                    print("%s" % (buffersize))
                    
                    print("%s of %s" % (offset, filesize))
                    result.Offset = offset
                    result.File = transfer.SrcFile.Name
                    result.Part = f.read(buffersize)
                    yield result
                    print("Writing to %s (%s %s %s)" % (result.File, result.Offset, f.tell(), result.Part.__len__()))
                    offset+=buffersize
                    asyncio.sleep(1)
                f.close()
                print("File uploaded: %s %s %s %s" % (transfer,offset,srcfile,filesize))
        try:
            while not self.Quiting:

                logging.info("Uploading")
                response = await self._stub.FileTransferProcessUpload(ReadFile())
                logging.info("Uploaded")
        
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                print(f"Upload unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                print(f"Upload unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            else:
                print(f"Upload unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
        except Exception as e:
            print(f"Upload failed: ", e)
        except:
            print(f"Upload failed")
        
        logging.info("Upload finished")
        
            #stream FilePartInfo) returns(google.protobuf.Empty) {}
    async def FileTransferProcessDownload(self):
        
        print("Started downloading")
        def WriteFile(write: Transfer.FilePartInfo):
            with open(write.File, "wb") as f:
                f.seek(write.Offset, 0)
                print("Writing to %s (%s %s %s)" % (write.File, write.Offset, f.tell(), write.Part.__len__()))
                f.write(write.Part)
                
            print("Writing to %s (%s %s)" % (write.File, write.Offset, write.Part.__len__()))
        try:
            print("Started downloading")
            while not self.Quiting:
                print("Started downloading")

                request = Empty()
                logging.info("downloading")
                async for response in self._stub.FileTransferProcessDownload(request):
                    print("actually downloading")
                    WriteFile(response)
            
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                print(f"Download unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                print(f"Download unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            else:
                print(f"Download unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
        except Exception as e:
            print(f"Download failed: ",e)
        except:
            print(f"Download failed")
        logging.info("Ended downloading")
        #google.protobuf.Empty) returns(stream FilePartInfo) {}
        
    async def FIleTransferProgress(self, req: Transfer.FileTransferRequestInit):
        logging.info("Started progress")
        #self.Tra.append(req)
        try:
            async for response in self._stub.FIleTransferProgress(req):
                print(response)
                await asyncio.sleep(1)
        
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                print(f"Progress unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                print(f"Progress unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            else:
                print(f"Progress unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
        except Exception as e:
            print(f"Progrss failed ", e)
        except:
            print(f"Progrss failed")
        
        print("returned")
        #returns(stream FileTransferProgress) {} 
        

    async def FileTransferListener(self):
        logging.info("Started")
        request = Empty()
        requests, respones = 0, 0
        async def Stream():
            nonlocal requests, respones
            while True:
                while requests-respones>=1:
                    await asyncio.sleep(1)
                logging.info("Received new upload request")
                requests += 1
                yield request


        logging.info("File transfer listens... %s", not self.Quiting)
        try:
            while not self.Quiting:
                logging.info("File transfer listens...")
                async for response in self._stub.FileTransferListener(Stream()):
                    print("File: ", response)
                    respones += 1
                    self.Transfers.append(response)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                print(f"Listener unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                print(f"Listener unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
                
            else:
                print(f"Listener unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}")
        except Exception as e:
            print(f"Listner Failed ", e)
        except:
            print(f"Listner failed")
        
        logging.info("File transfer listener")
        
        #stream google.protobuf.Empty) returns(stream FileTransferRequestInit) {} 