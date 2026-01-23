import asyncio
import json
from datetime import datetime
import websockets

HOST = "0.0.0.0"
PORT = 8765

clients = {}  # websocket -> {username, avatar}


async def send_user_list():
    count = len(clients)

    msg = json.dumps({
        "type": "user_list",
        "count": count
    })

    await asyncio.gather(
        *[ws.send(msg) for ws in clients],
        return_exceptions=True
    )


async def broadcast(message, sender=None):
    await asyncio.gather(
        *[
            ws.send(message)
            for ws in clients
            if ws != sender
        ],
        return_exceptions=True
    )


async def handler(websocket):
    try:
        # ===== Nhận info user =====
        raw = await websocket.recv()
        user_data = json.loads(raw)

        username = user_data["username"]
        avatar = user_data.get("avatar", "👤")

        clients[websocket] = {
            "username": username,
            "avatar": avatar
        }

        print(f"✅ {avatar} {username} connected")

        join_msg = json.dumps({
            "type": "system",
            "message": f"{avatar} {username} đã tham gia phòng chat",
            "time": datetime.now().strftime("%H:%M:%S")
        })

        await broadcast(join_msg, websocket)
        await send_user_list()

        # ===== Nhận tin nhắn =====
        async for raw_msg in websocket:
            data = json.loads(raw_msg)

            if data.get("type") == "message":
                msg = json.dumps({
                    "type": "message",
                    "username": username,
                    "avatar": avatar,
                    "message": data["message"],
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                await websocket.send(msg)
                await broadcast(msg, websocket)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        if websocket in clients:
            user = clients.pop(websocket)
            print(f"❌ {user['avatar']} {user['username']} disconnected")

            leave_msg = json.dumps({
                "type": "system",
                "message": f"{user['avatar']} {user['username']} đã rời khỏi phòng chat",
                "time": datetime.now().strftime("%H:%M:%S")
            })

            await broadcast(leave_msg)
            await send_user_list()


async def main():
    print(f"🚀 WebSocket Server running")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
