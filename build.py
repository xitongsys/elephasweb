#!/usr/bin/env python3
"""
构建脚本，用于将模板组合成最终的HTML文件
"""

import os
import re
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"
COMPONENTS_DIR = SRC_DIR / "components"
OUTPUT_DIR = PROJECT_ROOT / "dist"

# 页面配置
PAGES = {
    "index": {
        "title": "Elephas Investment",
        "description": "大音希声    大象无形",
        "content_file": "index_content.html",
        "styles": '<link rel="stylesheet" type="text/css" href="css/index.css">',
        "scripts": """
<script type="text/javascript" src="js/jquery.min_1.js"></script>
<script type="text/javascript" src="js/vue.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/region.js"></script>
<script type="text/javascript" src="js/common.js"></script>
<script type="text/javascript" charset="utf-8" src="js/form.js"></script>""",
        "footer_scripts": """
<script type="text/javascript" src="js/swiper.min.js"></script>
<script type="text/javascript">
//   if ($(".z_banner").length > 0) {
//     $(".z_banner_num .all").text("0" + $(".z_banner .bd li").length)
//     var _w = $('body').width(),
//         _w_2 = _w / 1,
//         time = 4000,
//         transition_time = 1200,
//         time_with_trans = (time + transition_time) / 1000;
//     $('.z_banner .imgbg').attr('data-swiper-parallax-x', _w_2)
//     var myBanner = new Swiper('.z_banner', {
//         loop: true,
// 		autoplay: true,
// 		delay: 1800,
// 		parallax: true,
// 		effect: "slide",
// 		speed: 1800,
// 		navigation: {
// 		  nextEl: '.next',
// 		  prevEl: '.prev',
// 	    },
//       on: {
//         slideChangeTransitionStart: function() {
//           $(".z_banner_num .index").text("0" + (this.realIndex + 1))
//         }
//       }
//     });
//   }
</script>"""
    },
    "about": {
        "title": "Elephas Investment",
        "description": "",
        "content_file": "about_content.html",
        "styles": '<link rel="stylesheet" type="text/css" href="css/index.css">',
        "scripts": """
<script type="text/javascript" src="js/jquery.min_1.js"></script>
<script type="text/javascript" src="js/vue.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/region.js"></script>
<script type="text/javascript" src="js/common.js"></script>
<script type="text/javascript" charset="utf-8" src="js/form.js"></script>""",
        "footer_scripts": """
<script src="js/countUp.min.js" type="text/javascript"></script>
<script src="js/swiper.min.js" type="text/javascript"></script>"""
    },
    "join": {
        "title": "Elephas Investment",
        "description": "",
        "content_file": "join_content.html",
        "styles": '<link rel="stylesheet" type="text/css" href="css/index.css">',
        "scripts": """
<script type="text/javascript" src="js/jquery.min_1.js"></script>
<script type="text/javascript" src="js/vue.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/region.js"></script>
<script type="text/javascript" src="js/common.js"></script>
<script type="text/javascript" charset="utf-8" src="js/form.js"></script>""",
        "footer_scripts": ""
    },
    "contact": {
        "title": "Elephas Investment",
        "description": "",
        "content_file": "contact_content.html",
        "styles": '<link rel="stylesheet" type="text/css" href="css/index.css">',
        "scripts": """
<script type="text/javascript" src="js/jquery.min_1.js"></script>
<script type="text/javascript" src="js/vue.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/region.js"></script>
<script type="text/javascript" src="js/common.js"></script>
<script type="text/javascript" charset="utf-8" src="js/form.js"></script>""",
        "footer_scripts": ""
    }
}

def read_file(path):
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"警告: 文件未找到: {path}")
        return ""

def write_file(path, content):
    """写入文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_page(page_name, config):
    """构建单个页面"""
    print(f"构建页面: {page_name}")

    # 读取基础模板
    base_template = read_file(TEMPLATES_DIR / "base.html")

    # 读取组件
    header = read_file(COMPONENTS_DIR / "header.html")
    modal = read_file(COMPONENTS_DIR / "modal.html")
    footer = read_file(COMPONENTS_DIR / "footer.html")

    # 读取内容
    content_file = TEMPLATES_DIR / config["content_file"]
    content = read_file(content_file)

    if not content:
        print(f"错误: 内容文件未找到: {content_file}")
        return

    # 替换占位符
    replacements = {
        "{{PAGE_TITLE}}": config["title"],
        "{{PAGE_DESCRIPTION}}": config["description"],
        "{{PAGE_STYLES}}": config["styles"],
        "{{PAGE_SCRIPTS}}": config["scripts"],
        "{{HEADER}}": header,
        "{{MODAL}}": modal,
        "{{CONTENT}}": content,
        "{{FOOTER}}": footer,
        "{{PAGE_FOOTER_SCRIPTS}}": config["footer_scripts"]
    }

    html = base_template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # 输出文件
    output_file = OUTPUT_DIR / f"{page_name}.html"
    write_file(output_file, html)
    print(f"  已生成: {output_file}")

def copy_assets():
    """复制静态资源"""
    print("复制静态资源...")

    # 复制CSS
    css_src = SRC_DIR / "css"
    css_dst = OUTPUT_DIR / "css"
    if css_src.exists():
        os.system(f"cp -r {css_src} {css_dst}")
        print(f"  复制CSS到: {css_dst}")

    # 复制JS
    js_src = SRC_DIR / "js"
    js_dst = OUTPUT_DIR / "js"
    if js_src.exists():
        os.system(f"cp -r {js_src} {js_dst}")
        print(f"  复制JS到: {js_dst}")

    # 复制assets
    assets_src = SRC_DIR / "assets"
    assets_dst = OUTPUT_DIR / "assets"
    if assets_src.exists():
        os.system(f"cp -r {assets_src} {assets_dst}")
        print(f"  复制assets到: {assets_dst}")

def main():
    """主函数"""
    print("开始构建 Elephas 网站...")

    # 创建输出目录
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 构建所有页面
    for page_name, config in PAGES.items():
        build_page(page_name, config)

    # 复制静态资源
    copy_assets()

    print("构建完成！")

if __name__ == "__main__":
    main()