# from flask import Flask, render_template, request, send_from_directory
# import os
# import time
# import subprocess
# import dashscope
# from dotenv import load_dotenv  # ✅ 引入 dotenv

# # ✅ 加载 .env 文件中的环境变量
# load_dotenv()

# app = Flask(__name__)

# # 视频输出目录
# VIDEO_DIR = os.path.join('static', 'videos')
# os.makedirs(VIDEO_DIR, exist_ok=True)

# # 模板文件读取
# def load_prompt_template():
#     path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
#     if not os.path.exists(path):
#         return None
#     with open(path, 'r', encoding='utf-8') as f:
#         return f.read()

# # 调用千问大模型
# def call_ai_model(prompt):
#     print("[调用大模型中] prompt:", prompt)
#     try:
#         response = dashscope.Generation.call(
#             model='qwen-turbo',
#             prompt=prompt,
#             result_format='message',
#             api_key=os.environ["DASHSCOPE_API_KEY"]
#         )
#     except Exception as e:
#         print("[异常] 调用失败:", e)
#         return fallback_code()

#     if response.status_code == 200:
#         raw = None
#         if response.output.get("text"):
#             raw = response.output["text"]
#         elif response.output.get("choices") and response.output["choices"][0]["message"].get("content"):
#             raw = response.output["choices"][0]["message"]["content"]

#         if raw:
#             print("[返回结果]:", raw)
#             return raw.replace("```python", "").replace("```", "").strip()

#     print("[错误] 千问未返回有效代码，返回信息：", response)
#     return fallback_code()

# def fallback_code():
#     return """from manim import *

# class TestScene(Scene):
#     def construct(self):
#         self.add(Text('生成失败，请稍后再试'))"""

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     user_input = request.form.get('description', '')
#     if not user_input.strip():
#         return render_template('index.html', error="❗请输入内容")

#     prompt_template = load_prompt_template()
#     if not prompt_template:
#         return render_template('index.html', error="⚠️ 缺少 prompt_template.txt 文件")

#     full_prompt = prompt_template.replace('{description}', user_input)

#     manim_code = call_ai_model(full_prompt)

#     timestamp = str(int(time.time()))
#     temp_script = f"temp_{timestamp}.py"
#     with open(temp_script, 'w', encoding='utf-8') as f:
#         f.write(manim_code)

#     output_path = os.path.join(VIDEO_DIR, f"output_{timestamp}.mp4")
#     render_cmd = f"manim {temp_script} TestScene -qk --media_dir static --output_file output_{timestamp}.mp4"
#     subprocess.run(render_cmd, shell=True)

#     os.remove(temp_script)

#     return render_template('index.html', video_file=f"output_{timestamp}.mp4")

# @app.route('/videos/<filename>')
# def serve_video(filename):
#     return send_from_directory(VIDEO_DIR, filename)

# # ✅ 用于部署环境：绑定到 0.0.0.0，并使用 Render 分配的端口
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))  # Render 会自动提供 PORT 环境变量
#     app.run(host='0.0.0.0', port=port)
# manim_patch.py





from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import time
import subprocess
import dashscope
from dotenv import load_dotenv
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# 加载 .env 环境变量
load_dotenv()

app = Flask(__name__)

# 视频输出目录
VIDEO_DIR = os.path.join('static', 'videos')
# 确保目录存在
os.makedirs(VIDEO_DIR, exist_ok=True)

# 读取 prompt 模板
def load_prompt_template():
    path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# 调用千问大模型
def call_ai_model(prompt):
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            result_format='message',
            api_key=os.environ.get("DASHSCOPE_API_KEY")
        )
    except Exception as e:
        print("[异常] 调用失败:", e)
        return fallback_code()

    if hasattr(response, 'status_code') and response.status_code == 200:
        raw = None
        if response.output.get("text"):
            raw = response.output["text"]
        elif response.output.get("choices"):
            raw = response.output["choices"][0]["message"].get("content")
        if raw:
            return raw.replace("```python", "").replace("```", "").strip()
    return fallback_code()

# 失败 fallback
def fallback_code():
    return """from manim import *

class TestScene(Scene):
    def construct(self):
        self.add(Text('生成失败，请稍后再试', font='Microsoft YaHei'))"""

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

    # 三维场景示例内置
    if '三维' in user_input or '旋转' in user_input:
        manim_code = '''from manim import *

class TestScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        sphere = Sphere(radius=0.2, color=RED).shift(UP * 3)
        self.add(sphere)

        self.play(sphere.animate.shift(DOWN * 5), run_time=3, rate_func=linear)

        self.stop_ambient_camera_rotation()
        self.wait()
'''
    else:
        manim_code = call_ai_model(full_prompt)
        # 统一类名为 TestScene
        manim_code = manim_code.replace("class ", "#class ").replace("FreeFall3D", "TestScene").replace("#class ", "class ")

    # 写入临时脚本
    timestamp = str(int(time.time()))
    temp_script = f"temp_{timestamp}.py"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(manim_code)

    # 渲染命令
    output_filename = f"output_{timestamp}.mp4"
    output_path = os.path.join(VIDEO_DIR, output_filename)
    render_cmd = (
        f"manim {temp_script} TestScene -qk --media_dir static --output_file {output_filename}"
    )
    subprocess.run(render_cmd, shell=True)

    # 尝试移动生成的视频到 static/videos
    temp_dir = os.path.join(VIDEO_DIR, f"temp_{timestamp}", "2160p60")
    rendered = os.path.join(temp_dir, output_filename)
    if os.path.exists(rendered):
        os.rename(rendered, output_path)

    # 清理临时脚本
    os.remove(temp_script)

    return render_template('index.html', video_file=output_filename)

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

# 智能关键词提取
def extract_keywords(text, top_k=5):
    words = [" ".join(jieba.lcut(text))]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(words)
    scores = zip(vectorizer.get_feature_names_out(), tfidf.toarray()[0])
    return [w for w, _ in sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]]

@app.route('/keywords', methods=['POST'])
def keywords():
    text = request.form.get('text', '')
    if not text.strip():
        return jsonify({'error': '内容不能为空'}), 400
    return jsonify({'keywords': extract_keywords(text)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
