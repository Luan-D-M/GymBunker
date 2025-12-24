from grpclib.client import Channel

from proto.usermanagement.v1 import UserManagementServiceStub as Stub

# ToDo: Performance improvement: one global channel when FastAPI starts and reuse it.
# Right now, it is openning a new Channel for every single request (slow).

async def create_user(user_id: str):
    channel = Channel(host='0.0.0.0', port=4000)
    service = Stub(channel)
    await service.create_user(id=user_id)
    channel.close()

async def delete_user(user_id: str):
    channel = Channel(host='0.0.0.0', port=4000)
    service = Stub(channel)
    await service.delete_user(id=user_id)
    channel.close()