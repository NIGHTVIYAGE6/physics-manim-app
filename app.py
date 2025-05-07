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




# from flask import Flask, render_template, request, send_from_directory, jsonify
# import os
# import time
# import subprocess
# import dashscope
# from dotenv import load_dotenv
# import jieba
# from sklearn.feature_extraction.text import TfidfVectorizer

# # 加载 .env
# load_dotenv()

# app = Flask(__name__)

# VIDEO_DIR = os.path.join('static', 'videos')
# os.makedirs(VIDEO_DIR, exist_ok=True)

# def load_prompt_template():
#     path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
#     if not os.path.exists(path):
#         return None
#     with open(path, 'r', encoding='utf-8') as f:
#         return f.read()

# def call_ai_model(prompt):
#     try:
#         resp = dashscope.Generation.call(
#             model='qwen-turbo',
#             prompt=prompt,
#             result_format='message',
#             api_key=os.environ["DASHSCOPE_API_KEY"]
#         )
#     except Exception as e:
#         print("AI 调用失败:", e)
#         return "// 调用失败，请稍后再试"
#     if resp.status_code == 200 and resp.output.get("text"):
#         return resp.output["text"]
#     return "// 未能生成代码，请重试"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     desc = request.form.get('description', '').strip()
#     if not desc:
#         return render_template('index.html', error="请输入内容")
#     template = load_prompt_template()
#     if not template:
#         return render_template('index.html', error="缺少 prompt_template.txt")

#     full_prompt = template.replace('{description}', desc)
#     if '三维' in desc or '旋转' in desc:
#         code = '''from manim import *
# class TestScene(ThreeDScene):
#     def construct(self):
#         axes = ThreeDAxes()
#         self.add(axes)
#         self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
#         self.begin_ambient_camera_rotation(rate=0.1)
#         sphere = Sphere(radius=0.2, color=RED).shift(UP * 3)
#         self.add(sphere)
#         self.play(sphere.animate.shift(DOWN * 5), run_time=3, rate_func=linear)
#         self.stop_ambient_camera_rotation()
#         self.wait()
# '''
#     else:
#         code = call_ai_model(full_prompt)

#     # 写临时脚本
#     ts = str(int(time.time()))
#     script_name = f"temp_{ts}.py"
#     with open(script_name, 'w', encoding='utf-8') as f:
#         f.write(code)

#     # 渲染到 static/videos 下
#     output_name = f"output_{ts}.mp4"
#     cmd = (
#         f"manim {script_name} TestScene -ql "
#         f"--media_dir {VIDEO_DIR} --output_file {output_name}"
#     )
#     subprocess.run(cmd, shell=True)
#     os.remove(script_name)

#     # ====== 这一行把生成的文件从子目录搬到 videos 根目录 ======
#     src = os.path.join(VIDEO_DIR, 'videos', f"temp_{ts}", '480p15', output_name)
#     dst = os.path.join(VIDEO_DIR, output_name)
#     if os.path.exists(src):
#         os.replace(src, dst)

#     return render_template('index.html', video_file=output_name)

# @app.route('/videos/<filename>')
# def serve_video(filename):
#     return send_from_directory(VIDEO_DIR, filename)

# def extract_keywords(text, top_k=5):
#     tokens = [" ".join(jieba.lcut(text))]
#     vec = TfidfVectorizer()
#     tfidf = vec.fit_transform(tokens)
#     scores = zip(vec.get_feature_names_out(), tfidf.toarray()[0])
#     return [w for w,_ in sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]]

# @app.route('/keywords', methods=['POST'])
# def keywords():
#     text = request.form.get('text', '').strip()
#     if not text:
#         return jsonify({'error': '内容不能为空'}), 400
#     return jsonify({'keywords': extract_keywords(text)})

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)





from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import time
import subprocess
import requests
import dashscope
from dotenv import load_dotenv
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# 加载 .env 中的所有环境变量
load_dotenv()

app = Flask(__name__)

# 视频输出目录
VIDEO_DIR = os.path.join('static', 'videos')
os.makedirs(VIDEO_DIR, exist_ok=True)

def load_prompt_template():
    path = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def call_ai_model(prompt):
    try:
        resp = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            result_format='message',
            api_key=os.getenv("DASHSCOPE_API_KEY")
        )
    except Exception as e:
        print("AI 调用失败:", e)
        return "// 调用失败，请稍后再试"
    if resp.status_code == 200 and resp.output.get("text"):
        return resp.output["text"]
    return "// 未能生成代码，请重试"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    desc = request.form.get('description', '').strip()
    if not desc:
        return render_template('index.html', error="请输入内容")
    template = load_prompt_template()
    if not template:
        return render_template('index.html', error="缺少 prompt_template.txt")

    full_prompt = template.replace('{description}', desc)
    if '三维' in desc or '旋转' in desc:
        code = '''from manim import *
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
        code = call_ai_model(full_prompt)

    # 写入临时脚本
    ts = str(int(time.time()))
    script_name = f"temp_{ts}.py"
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(code)

    # 渲染到 static/videos 下
    output_name = f"output_{ts}.mp4"
    cmd = (
        f"manim {script_name} TestScene -ql "
        f"--media_dir {VIDEO_DIR} --output_file {output_name}"
    )
    subprocess.run(cmd, shell=True)
    os.remove(script_name)

    # 将生成文件从子目录搬到 videos 根目录
    src = os.path.join(VIDEO_DIR, 'videos', f"temp_{ts}", '480p15', output_name)
    dst = os.path.join(VIDEO_DIR, output_name)
    if os.path.exists(src):
        os.replace(src, dst)

    # 把用户输入回传给模板，以便页面刷新后重新触发关键词、示意图和动画展示
    return render_template(
        'index.html',
        video_file=output_name,
        description=desc
    )

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

@app.route('/keywords', methods=['POST'])
def keywords():
    text = request.form.get('text', '').strip()
    if not text:
        return jsonify({'error': '内容不能为空'}), 400
    tokens = [" ".join(jieba.lcut(text))]
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(tokens)
    scores = zip(vec.get_feature_names_out(), tfidf.toarray()[0])
    keywords = [w for w, _ in sorted(scores, key=lambda x: x[1], reverse=True)[:5]]
    return jsonify({'keywords': keywords})

@app.route('/images', methods=['POST'])
def fetch_images():
    data = request.get_json(force=True)
    keywords = data.get("keywords", [])
    if not keywords:
        return jsonify({"error": "keywords list is empty"}), 400

    # 在原有关键词后追加“物理 示意图 diagram physics”
    core = " ".join(keywords)
    query = f"{core} 物理 示意图 diagram physics"
    url    = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": 6,
        "orientation": "landscape",
    }
    headers = {
        "Authorization": f"Client-ID {os.getenv('UNSPLASH_ACCESS_KEY')}"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        images = [img["urls"]["small"] for img in results]
    except Exception as e:
        app.logger.error("Unsplash API error: %s", e)
        return jsonify({"error": "failed to fetch images"}), 502

    return jsonify({"images": images})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(force=True)
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'answer': '问题不能为空'}), 400

    # 简易 FAQ 知识库
    faq = {
        '牛顿第二定律': '牛顿第二定律表明：一个物体的加速度与施加在它上面的合力成正比，与其质量成反比，即 F=ma。',
        '自由落体': '自由落体是在重力作用下的运动，忽略空气阻力时，其加速度约为 9.8 m/s²。',
        # 可以根据需要继续补充更多常见问答
    }
    for key, ans in faq.items():
        if key in question:
            return jsonify({'answer': ans})

    # 未命中 FAQ，fallback 调用大模型
    prompt = f"请简要回答以下物理教学问题：\n问题：{question}\n回答："
    ai_response = call_ai_model(prompt)
    return jsonify({'answer': ai_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

