from flask import Flask, render_template, request, send_from_directory
import os
import time
import subprocess
import dashscope
from dotenv import load_dotenv  # ✅ 引入 dotenv

# ✅ 加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)

# 视频输出目录
VIDEO_DIR = os.path.join('static', 'videos')
os.makedirs(VIDEO_DIR, exist_ok=True)

# 模板文件读取
def load_prompt_template():
    path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 调用千问大模型
def call_ai_model(prompt):
    print("[调用大模型中] prompt:", prompt)
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            result_format='message',
            api_key=os.environ["DASHSCOPE_API_KEY"]
        )
    except Exception as e:
        print("[异常] 调用失败:", e)
        return fallback_code()

    if response.status_code == 200:
        raw = None
        if response.output.get("text"):
            raw = response.output["text"]
        elif response.output.get("choices") and response.output["choices"][0]["message"].get("content"):
            raw = response.output["choices"][0]["message"]["content"]

        if raw:
            print("[返回结果]:", raw)
            return raw.replace("```python", "").replace("```", "").strip()

    print("[错误] 千问未返回有效代码，返回信息：", response)
    return fallback_code()

def fallback_code():
    return """from manim import *

class TestScene(Scene):
    def construct(self):
        self.add(Text('生成失败，请稍后再试'))"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form.get('description', '')
    if not user_input.strip():
        return render_template('index.html', error="❗请输入内容")

    prompt_template = load_prompt_template()
    if not prompt_template:
        return render_template('index.html', error="⚠️ 缺少 prompt_template.txt 文件")

    full_prompt = prompt_template.replace('{description}', user_input)

    manim_code = call_ai_model(full_prompt)

    timestamp = str(int(time.time()))
    temp_script = f"temp_{timestamp}.py"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(manim_code)

    output_path = os.path.join(VIDEO_DIR, f"output_{timestamp}.mp4")
    render_cmd = f"manim {temp_script} TestScene -qk --media_dir static --output_file output_{timestamp}.mp4"
    subprocess.run(render_cmd, shell=True)

    os.remove(temp_script)

    return render_template('index.html', video_file=f"output_{timestamp}.mp4")

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

# ✅ 用于部署环境：绑定到 0.0.0.0，并使用 Render 分配的端口
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render 会自动提供 PORT 环境变量
    app.run(host='0.0.0.0', port=port)
