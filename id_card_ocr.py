import os
import requests
import json
import base64

# API endpoint
url = "http://192.168.6.198:8080/v1/chat/completions"

# Image path
image_path = "/home/py/test_claude/test_id_card_sample.jpg"  # Test image

# Read and encode image as base64
def encode_image_to_base64(image_path):
    """Encode image file to base64 data URL"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded}"

# Request payload with base64 encoded image
image_base64 = encode_image_to_base64(image_path)

data = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_base64},
                },
                {
                    "type": "text",
                    "text": """请按下列JSON格式输出图中信息:
{
"身份证号": "",
"姓名": "",
"性别": "",
"出生日期": "",
"民族":"",
"地址": "",
"有效期限": "",
"签发机关": ""
}""",
                },
            ],
        }
    ]
}

# Optional: Add model parameter if needed
# data["model"] = "your-model-name"

# Make the POST request
try:
    response = requests.post(url, json=data, timeout=60)
    response.raise_for_status()

    # Parse and display the result
    result = response.json()
    print("Response:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Extract the content if the response follows OpenAI format
    if "choices" in result and len(result["choices"]) > 0:
        content = result["choices"][0]["message"]["content"]
        print("\nExtracted ID Card Info:")
        print(content)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON response: {e}")
