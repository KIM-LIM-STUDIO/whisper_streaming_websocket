# Whisper Streaming with WebSocket

이 프로젝트는 [Whisper Streaming](https://github.com/ufal/whisper_streaming) 구현을 확장하여 실시간 AI 생성 시청자 댓글 기능을 추가한 버전입니다.

## 실행 방법

### 📌 요구사항 설치
#### 1️⃣ **Python 패키지 설치**
```bash
pip install -r requirements.txt
```
#### 2️⃣ **Mac 터미널에서 FFmpeg 설치**
```bash
brew install ffmpeg
```

### 1️⃣ 실시간 음성 인식 모델 실행 (Whisper Streaming 서버)
```bash
python3 whisper_online_server.py --backend mlx-whisper --language ko --vac --model small
```
이 명령어는 Whisper 스트리밍 서버를 실행하여 실시간 오디오 입력을 받아 텍스트로 변환합니다.

### 2️⃣ 가상 시청자 WebSocket 서버 실행
```bash
python3 virtual_viewers.py
```
이 스크립트는 Whisper에서 변환된 텍스트를 받아 OpenAI API를 이용해 가상 시청자 댓글을 생성한 후 WebSocket을 통해 클라이언트(예: React 프론트엔드)로 전송합니다.

### 3️⃣ FFmpeg를 사용하여 실시간 오디오 입력 제공
```bash
ffmpeg -f avfoundation -i ":0" -ac 1 -ar 16000 -f wav - | nc localhost 43007
```
이 명령어는 마이크 입력을 캡처하고, 16kHz 모노 WAV 형식으로 변환한 후 Whisper 서버(포트 `43007`)로 스트리밍합니다.

## 요약

- **Whisper Streaming**: 실시간 오디오를 처리하고 텍스트로 변환합니다.
- **가상 시청자 WebSocket 서버**: 변환된 텍스트를 받아 AI 기반 가상 시청자 댓글을 생성합니다.
- **FFmpeg**: 마이크 입력을 캡처하여 Whisper로 스트리밍합니다.

이 설정을 통해 실시간 음성 인식과 AI 기반 시청자 상호작용이 가능한 스트리밍 환경을 구축할 수 있습니다.

##  본 프로젝트는 Mac 환경에서 실행됩니다.


## 활용예시

![image](https://github.com/user-attachments/assets/bd6e8f2c-1144-42e3-95dc-1b83ab1976de)


