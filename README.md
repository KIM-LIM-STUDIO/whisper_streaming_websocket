# Whisper Streaming with  WebSocket 

This project extends the [Whisper Streaming](https://github.com/ufal/whisper_streaming) implementation by incorporating few extras.

#작동방식 example
1.python3 whisper_online_server.py --backend mlx-whisper --language ko --vac --model small (실시간 음성 인식 모델)
2.python3 virtual_viewers.py ( whisper에서 받은 텍스트 openai-api 이용해 가상 시청자 댓글 생성)
3.음성 입력을 위해 터미널에서 ffmpeg -f avfoundation -i ":0" -ac 1 -ar 16000 -f wav - | nc localhost 43007 (마이크 샘플링 레이트 16000hz로 입력 받아서 whisper 전송) 


