After installing requirements.txt in a venv, the following command generated the files:

```
python3 -m grpc_tools.protoc -I . --python_betterproto_out=. user_management.proto
```