import os
from typing import List, Tuple
from cx_Freeze import setup, Executable

proj_root = os.path.abspath(os.path.dirname(__file__))

# 需要打包的额外文件
include_files: List[Tuple[str, str]] = [
    (os.path.join(proj_root, 'config.yml'), 'config.yml'),
    (os.path.join(proj_root, 'data'), 'data'),
    (os.path.join(proj_root, 'image'), 'image')
]

# 包含 Python 代码模块
includes = []
web_path = os.path.join(proj_root, 'javsp', 'web')
if os.path.exists(web_path):
    for file in os.listdir(web_path):
        name, ext = os.path.splitext(file)
        if ext == '.py':
            includes.append(f'javsp.web.{name}')

# 依赖的 Python 包
packages = ['pendulum']  # pydantic_extra_types 依赖 pendulum

# cx_Freeze 配置
build_exe = {
    'include_files': include_files,
    'includes': includes,
    'excludes': ['unittest', 'tkinter', 'win32crypt'],  # 排除不需要的库（如 tkinter, win32crypt）
    'packages': packages,
    'optimize': 2,  # 优化生成的可执行文件（减少文件大小）
    'build_exe': 'build_linux_arm64',  # 可以设置目标平台的特定输出文件夹
}

# 生成 Linux (ARM64) 可执行文件
javsp = Executable(
    script=os.path.join(proj_root, 'javsp', '__main__.py'),
    target_name='JavSP',  # 生成可执行文件名（不要加 .exe）
    base=None,  # Linux 不需要 Win32GUI
)

setup(
    name='JavSP',
    options={'build_exe': build_exe},
    executables=[javsp]
)