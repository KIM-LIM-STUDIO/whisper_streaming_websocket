import asyncio
import websockets
import json
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(" ERROR: OpenAI API 키가 환경 변수에서 로드되지 않았습니다.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# WebSocket 서버 설정
VIRTUAL_VIEWERS_HOST = "localhost"
VIRTUAL_VIEWERS_PORT = 8765
CLIENT_PORT = 8766  # 클라이언트용 WebSocket 포트

# WebSocket에 연결된 클라이언트들 저장
connected_clients = set()

async def generate_ai_response(message):
    """ OpenAI API를 호출하여 가상 시청자 댓글 생성 """
    system_prompt = """
    너는 가상 시청자야. 스트리머의 생방송을 보고 실시간으로 채팅하는 역할을 해.
    각각 다른 닉네임을 가진 5명의 시청자처럼 반응해줘.

    형식 예시:
    [닉네임1]: "방송 개꿀잼!"
    [닉네임2]: "아ㅋㅋ 개웃기네 ㄹㅇㅋㅋㅋ"
    [닉네임3]: "오늘 컨디션 좀 좋아보이누!"
    [닉네임4]: "와 개레전드!"
    [닉네임5]: "다음 콘텐츠도 기대한다!"

    이제 스트리머의 발언을 듣고, 5명의 시청자처럼 채팅을 남겨줘.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content.strip()
        chat_responses = []
        
        for line in ai_response.split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                username = parts[0].strip()
                chat_message = parts[1].strip()
                chat_responses.append({"username": username, "message": chat_message})

        return chat_responses
    except Exception as e:
        print(f" OpenAI API 오류: {e}")
        return []

async def handle_whisper_message(websocket):
    """ Whisper 서버에서 WebSocket으로 전송된 텍스트를 수신하고 AI 가상 시청자 댓글 생성 """
    print(f" Whisper 서버 연결됨 (클라이언트: {websocket.remote_address})")
    try:
        async for message in websocket:
            data = json.loads(message)
            text = data.get("text", "").strip()
            print(f" Whisper 변환 텍스트 수신: {text}")

            if not text:
                print(" 수신한 텍스트가 없음. 건너뜀.")
                continue

            # OpenAI API를 호출하여 가상 시청자 댓글 생성
            chat_responses = await generate_ai_response(text)

            # 생성된 가상 시청자 댓글 출력
            for response in chat_responses:
                chat_message = f"[{response['username']}] {response['message']}"
                print(f"AI 시청자 댓글: {chat_message}")

            # 연결된 모든 WebSocket 클라이언트에게 메시지 전송
            if connected_clients:
                json_message = json.dumps(chat_responses, ensure_ascii=False)
                await asyncio.gather(*[ws.send(json_message) for ws in connected_clients if not ws.closed])

    except websockets.exceptions.ConnectionClosed:
        print(" Whisper 서버 연결 해제")
    except Exception as e:
        print(f" 오류 발생 (Whisper 처리 중): {e}")

async def handle_client(websocket):
    """ WebSocket 클라이언트 (프론트엔드) 관리 """
    print(f" 클라이언트 연결됨 (주소: {websocket.remote_address})")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"클라이언트 메시지 수신: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("클라이언트 연결 해제")
    finally:
        connected_clients.remove(websocket)

async def start_websocket_server():
    """ WebSocket 서버 실행 """
    try:
        async with websockets.serve(handle_whisper_message, VIRTUAL_VIEWERS_HOST, VIRTUAL_VIEWERS_PORT) as whisper_server, \
                   websockets.serve(handle_client, VIRTUAL_VIEWERS_HOST, CLIENT_PORT) as client_server:
            
            print(f" virtual_viewers.py WebSocket 서버 실행 중: ws://{VIRTUAL_VIEWERS_HOST}:{VIRTUAL_VIEWERS_PORT}")
            print(f" WebSocket 클라이언트 접속 대기 중: ws://{VIRTUAL_VIEWERS_HOST}:{CLIENT_PORT}")

            await asyncio.Future()  # 서버가 종료되지 않도록 무한 대기

    except Exception as e:
        print(f" WebSocket 서버 실행 오류: {e}")

if __name__ == "__main__":
    asyncio.run(start_websocket_server())  #  서버 실행
