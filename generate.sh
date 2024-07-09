python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./protos/Files.proto
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./protos/Transfer.proto
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./protos/User.proto