import requests
from sseclient import SSEClient
import os
import json


def stream_chat():
    # 检查API密钥
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("错误: 请设置 API_KEY 环境变量")
        return
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "user", "content": "请用 Python 写一个快速排序"}
    ]
    
    payload = {
        "model": "deepseek-coder",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 512,
        "stream": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()  # 检查HTTP错误
        
        client = SSEClient(response)
        
        for event in client.events():
            if event.data.strip() == "[DONE]":
                break
            try:
                # 解析JSON数据
                data = json.loads(event.data)
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    if 'content' in delta:
                        print(delta['content'], end='', flush=True)
            except json.JSONDecodeError:
                # 如果不是有效的JSON，跳过
                continue
            
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    stream_chat()
