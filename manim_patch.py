# manim_patch.py
import manim.utils.tex_file_writing as tex_writing

def patched_print_all_tex_errors(tex_compilation_log, error_indices, tex_file):
    error_patterns = [
        r"! (?P<error>.+)",
        r"(?P<error>Missing \$ inserted)",
        r"(?P<error>Paragraph ended before .+ was complete)",
    ]
    if error_indices:
        # 使用 utf-8 编码读取文件
        with open(tex_file, 'r', encoding='utf-8') as f:
            tex = f.readlines()
        for error_index in error_indices:
            tex_writing.print_tex_error(tex_compilation_log, error_index, tex)

# 替换原函数
tex_writing.print_all_tex_errors = patched_print_all_tex_errors