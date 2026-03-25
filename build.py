#!/usr/bin/env python3
"""
构建脚本，用于将模板组合成最终的HTML文件
"""

import os
import re
import json
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"
COMPONENTS_DIR = SRC_DIR / "components"
I18N_DIR = SRC_DIR / "i18n"
OUTPUT_DIR = PROJECT_ROOT / "dist"

# 支持的语言
SUPPORTED_LANGUAGES = ['zh-CN', 'en-US']
DEFAULT_LANGUAGE = 'zh-CN'

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

def load_translations():
    """加载所有语言的翻译数据"""
    translations = {}
    for lang_code in SUPPORTED_LANGUAGES:
        translation_file = I18N_DIR / f"{lang_code}.json"
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                translations[lang_code] = json.load(f)
            print(f"  加载翻译: {lang_code}")
        except FileNotFoundError:
            print(f"错误: 翻译文件未找到: {translation_file}")
            translations[lang_code] = {}
        except json.JSONDecodeError as e:
            print(f"错误: 翻译文件格式错误 {translation_file}: {e}")
            translations[lang_code] = {}
    return translations

def replace_i18n_placeholders(content, translations, lang_code):
    """替换内容中的i18n占位符为对应语言的翻译"""
    # 正则匹配 {{i18n.key.path}} 格式的占位符
    pattern = r'\{\{i18n\.([^}]+)\}\}'

    def replace_match(match):
        key_path = match.group(1)  # 例如 "global.nav_home"
        # 从翻译数据中获取值
        value = get_nested_value(translations.get(lang_code, {}), key_path.split('.'))
        if value is None:
            # 如果没有找到翻译，尝试从默认语言获取
            default_value = get_nested_value(translations.get(DEFAULT_LANGUAGE, {}), key_path.split('.'))
            if default_value is None:
                print(f"警告: 未找到翻译键: {key_path} (语言: {lang_code})")
                return f"[{key_path}]"  # 返回键作为占位符
            return default_value
        return value

    # 替换所有匹配的占位符
    return re.sub(pattern, replace_match, content)

def get_nested_value(data, key_parts):
    """从嵌套字典中获取值"""
    value = data
    for key in key_parts:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value

def write_file(path, content):
    """写入文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_page(page_name, config, lang_code, translations):
    """构建单个页面的多语言版本"""
    print(f"构建页面: {page_name} (语言: {lang_code})")

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

    # 应用翻译到所有内容
    content = replace_i18n_placeholders(content, translations, lang_code)
    header = replace_i18n_placeholders(header, translations, lang_code)
    modal = replace_i18n_placeholders(modal, translations, lang_code)
    footer = replace_i18n_placeholders(footer, translations, lang_code)

    # 页面标题和描述可能需要根据语言调整
    # 这里可以扩展配置以支持不同语言的标题
    page_title = config.get("title", "Elephas Investment")
    page_description = config.get("description", "")

    # 获取当前语言的翻译数据并转换为JSON字符串
    # 注意：需要确保JSON字符串对JavaScript安全
    import json
    i18n_data_json = json.dumps(translations.get(lang_code, {}))

    # 替换占位符
    replacements = {
        "{{PAGE_TITLE}}": page_title,
        "{{PAGE_DESCRIPTION}}": page_description,
        "{{PAGE_STYLES}}": config["styles"],
        "{{PAGE_SCRIPTS}}": config["scripts"],
        "{{HEADER}}": header,
        "{{MODAL}}": modal,
        "{{CONTENT}}": content,
        "{{FOOTER}}": footer,
        "{{PAGE_FOOTER_SCRIPTS}}": config["footer_scripts"],
        "{{I18N_DATA}}": i18n_data_json,
        "{{CURRENT_LANGUAGE}}": lang_code
    }

    html = base_template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # 输出到语言特定目录
    lang_output_dir = OUTPUT_DIR / lang_code
    output_file = lang_output_dir / f"{page_name}.html"
    write_file(output_file, html)
    print(f"  已生成: {output_file}")

def copy_assets():
    """复制静态资源"""
    print("复制静态资源...")

    # 复制CSS
    css_src = SRC_DIR / "css"
    css_dst = OUTPUT_DIR / "css"
    if css_src.exists():
        os.makedirs(css_dst, exist_ok=True)
        os.system(f"cp -r {css_src}/. {css_dst}/")
        print(f"  复制CSS到: {css_dst}")

    # 复制JS
    js_src = SRC_DIR / "js"
    js_dst = OUTPUT_DIR / "js"
    if js_src.exists():
        os.makedirs(js_dst, exist_ok=True)
        os.system(f"cp -r {js_src}/. {js_dst}/")
        print(f"  复制JS到: {js_dst}")

    # 复制assets
    assets_src = SRC_DIR / "assets"
    assets_dst = OUTPUT_DIR / "assets"
    if assets_src.exists():
        os.makedirs(assets_dst, exist_ok=True)
        os.system(f"cp -r {assets_src}/. {assets_dst}/")
        print(f"  复制assets到: {assets_dst}")

def create_redirect_page():
    """创建根目录重定向页面，根据用户偏好跳转到对应语言"""
    redirect_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Elephas Investment - Redirecting</title>
    <script>
        // 语言检测优先级: 1. localStorage 2. cookie 3. 浏览器语言 4. 默认中文
        function getPreferredLanguage() {
            // 检查localStorage
            var storedLang = localStorage.getItem('preferred_lang');
            if (storedLang && (storedLang === 'zh-CN' || storedLang === 'en-US')) {
                return storedLang;
            }

            // 检查cookie
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.startsWith('lang=')) {
                    var langValue = cookie.substring(5);
                    if (langValue === 'zh-CN' || langValue === 'en-US') {
                        return langValue;
                    }
                }
            }

            // 检查浏览器语言
            var browserLang = navigator.language || navigator.userLanguage;
            if (browserLang.startsWith('zh')) {
                return 'zh-CN';
            } else {
                return 'en-US';
            }
        }

        // 重定向到首选语言
        var preferredLang = getPreferredLanguage();
        window.location.href = '/' + preferredLang + '/index.html';
    </script>
</head>
<body>
    <p>正在跳转到您的首选语言...</p>
    <noscript>
        <p>请启用JavaScript以获得最佳体验，或手动选择语言：</p>
        <ul>
            <li><a href="/zh-CN/index.html">中文</a></li>
            <li><a href="/en-US/index.html">English</a></li>
        </ul>
    </noscript>
</body>
</html>'''

    output_file = OUTPUT_DIR / "index.html"
    write_file(output_file, redirect_html)
    print(f"  已生成根目录重定向页面: {output_file}")

def main():
    """主函数"""
    print("开始构建 Elephas 多语言网站...")

    # 加载翻译数据
    print("加载翻译数据...")
    translations = load_translations()

    if not translations:
        print("错误: 无法加载翻译数据，构建终止")
        return

    # 创建输出目录
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 为每种语言构建所有页面
    for lang_code in SUPPORTED_LANGUAGES:
        print(f"\n构建语言版本: {lang_code}")

        # 创建语言特定目录
        lang_output_dir = OUTPUT_DIR / lang_code
        lang_output_dir.mkdir(exist_ok=True)

        # 构建所有页面
        for page_name, config in PAGES.items():
            build_page(page_name, config, lang_code, translations)

    # 创建根目录重定向页面
    print("\n创建根目录重定向页面...")
    create_redirect_page()

    # 复制静态资源到所有语言目录
    print("\n复制静态资源...")
    for lang_code in SUPPORTED_LANGUAGES:
        lang_output_dir = OUTPUT_DIR / lang_code
        print(f"  复制到: {lang_output_dir}")

        # 复制CSS
        css_src = SRC_DIR / "css"
        css_dst = lang_output_dir / "css"
        if css_src.exists():
            os.makedirs(css_dst, exist_ok=True)
            os.system(f"cp -r {css_src}/. {css_dst}/")

        # 复制JS
        js_src = SRC_DIR / "js"
        js_dst = lang_output_dir / "js"
        if js_src.exists():
            os.makedirs(js_dst, exist_ok=True)
            os.system(f"cp -r {js_src}/. {js_dst}/")

        # 复制assets
        assets_src = SRC_DIR / "assets"
        assets_dst = lang_output_dir / "assets"
        if assets_src.exists():
            os.makedirs(assets_dst, exist_ok=True)
            os.system(f"cp -r {assets_src}/. {assets_dst}/")

    print("\n构建完成！")

if __name__ == "__main__":
    main()