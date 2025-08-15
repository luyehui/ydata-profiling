import contextlib
import warnings
from typing import Any

import matplotlib
import matplotlib.font_manager as fm
import seaborn as sns
from pandas.plotting import (
    deregister_matplotlib_converters,
    register_matplotlib_converters,
)


def get_chinese_fonts():
    """Get a list of fonts that support Chinese characters."""
    import platform
    import matplotlib.font_manager as fm
    import os
    
    system = platform.system()
    
    if system == "Windows":
        # Windows系统常见中文字体
        fonts = [
            "SimHei",  # 黑体 - 优先使用
            "Microsoft YaHei",  # 微软雅黑
            "SimSun",  # 宋体
            "KaiTi",  # 楷体
            "FangSong",  # 仿宋
            "Arial Unicode MS",  # Arial Unicode
        ]
        
        # 直接检查Windows字体文件
        font_dir = r"C:\Windows\Fonts"
        if os.path.exists(font_dir):
            # 检查字体文件是否存在
            font_files = {
                "SimHei": ["simhei.ttf"],  # 优先检查SimHei
                "Microsoft YaHei": ["msyh.ttc", "msyhbd.ttc"],
                "SimSun": ["simsun.ttc", "simsun.ttf"],
                "KaiTi": ["simkai.ttf"],
                "FangSong": ["simfang.ttf"],
            }
            
            available_fonts = []
            for font_name, file_names in font_files.items():
                for file_name in file_names:
                    if os.path.exists(os.path.join(font_dir, file_name)):
                        available_fonts.append(font_name)
                        break
            
            if available_fonts:
                return available_fonts
    
    elif system == "Darwin":  # macOS
        # macOS系统常见中文字体
        fonts = [
            "PingFang SC",  # 苹方
            "Hiragino Sans GB",  # 冬青黑体
            "STHeiti",  # 华文黑体
            "Arial Unicode MS",
        ]
    else:  # Linux
        # Linux系统常见中文字体
        fonts = [
            "WenQuanYi Micro Hei",  # 文泉驿微米黑
            "WenQuanYi Zen Hei",  # 文泉驿正黑
            "Noto Sans CJK SC",  # Noto Sans 中文简体
            "Noto Sans CJK TC",  # Noto Sans 中文繁体
            "DejaVu Sans",
        ]
    
    # 过滤出实际可用的字体
    available_fonts = []
    for font_name in fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            # 检查字体路径是否有效（不是默认回退字体）
            if font_path and font_path != fm.rcParams['font.sans-serif'][0]:
                available_fonts.append(font_name)
        except:
            continue
    
    return available_fonts


@contextlib.contextmanager
def manage_matplotlib_context() -> Any:
    """Return a context manager for temporarily changing matplotlib unit registries and rcParams."""
    originalRcParams = matplotlib.rcParams.copy()

    # Credits for this style go to the ggplot and seaborn packages.
    #   We copied the style file to remove dependencies on the Seaborn package.
    #   Check it out, it's an awesome library for plotting
    customRcParams = {
        "patch.facecolor": "#348ABD",  # blue
        "patch.antialiased": True,
        "font.size": 10.0,
        "figure.edgecolor": "0.50",
        # Seaborn common parameters
        "figure.facecolor": "white",
        "text.color": ".15",
        "axes.labelcolor": ".15",
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": ".15",
        "ytick.color": ".15",
        "axes.axisbelow": True,
        "image.cmap": "Greys",
        "font.family": ["sans-serif"],
        "font.sans-serif": ["SimHei", "Microsoft YaHei", "Arial", "Liberation Sans", "Bitstream Vera Sans", "sans-serif"],
        "grid.linestyle": "-",
        "lines.solid_capstyle": "round",
        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        "axes.grid": True,
        "axes.facecolor": "#EAEAF2",
        "axes.edgecolor": "white",
        "axes.linewidth": 0,
        "grid.color": "white",
        # Seaborn notebook context
        "figure.figsize": [8.0, 5.5],
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.linewidth": 1,
        "lines.linewidth": 1.75,
        "patch.linewidth": 0.3,
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        "backend": "agg",
        "axes.unicode_minus": False,  # 确保Unicode字符正确显示
    }

    try:
        register_matplotlib_converters()
        
        # 先设置字体，确保不被覆盖
        matplotlib.rcParams['font.family'] = ['sans-serif']
        matplotlib.rcParams['font.sans-serif'] = ["SimHei", "Microsoft YaHei", "Arial", "Liberation Sans", "Bitstream Vera Sans", "sans-serif"]
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        # 更新其他参数
        matplotlib.rcParams.update(customRcParams)
        
        # 应用seaborn样式，但立即重新设置字体
        sns.set_style(style="white")
        
        # 再次强制设置字体，确保不被seaborn覆盖
        matplotlib.rcParams['font.family'] = ['sans-serif']
        matplotlib.rcParams['font.sans-serif'] = ["SimHei", "Microsoft YaHei", "Arial", "Liberation Sans", "Bitstream Vera Sans", "sans-serif"]
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        yield
    finally:
        deregister_matplotlib_converters()  # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=matplotlib.MatplotlibDeprecationWarning
            )
            matplotlib.rcParams.update(originalRcParams)  # revert to original rcParams
