#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用稳定的真实玩具图片URL更新商品
使用Pixabay和Pexels的公开图片链接
"""

import re
from pathlib import Path

# 使用Pixabay和Pexels的真实玩具图片URL
# 这些是公开的、稳定的图片链接
REAL_TOY_IMAGE_URLS = {
    "变形金刚": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "玩具枪": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "漫威英雄": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "DC宇宙": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "毛绒玩具": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "幼儿积木": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "恐龙模型": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "拼图益智": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
}

def update_with_stable_images():
    """使用稳定的真实图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Pixabay的真实玩具图片
    # 这些是公开的、稳定的CDN链接
    category_urls = {
        "变形金刚": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
            "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
            "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        ],
        "玩具枪": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "漫威英雄": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        ],
        "DC宇宙": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        ],
        "毛绒玩具": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "幼儿积木": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "恐龙模型": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "拼图益智": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
    }
    
    # 查找所有商品
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"Found {len(matches)} products")
    
    updated_count = 0
    category_counts = {}
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
        index = category_counts[category] - 1
        
        # 获取该分类的图片URL列表
        urls = category_urls.get(category, category_urls["变形金刚"])
        # 循环使用URL，确保每个商品都有图片
        selected_url = urls[index % len(urls)]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 10:
                print(f"[{product_id}] {title} ({category})")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("Using Pixabay CDN - these are real toy photos")
        print("\nPlease clear browser cache (Ctrl+F5) and refresh the page")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Stable Real Toy Images")
    print("=" * 60)
    print("\nUsing Pixabay CDN for real toy photos\n")
    
    update_with_stable_images()
    
    print("\n" + "=" * 60)
    print("Done! Please clear cache (Ctrl+F5) and refresh")
    print("=" * 60)





# -*- coding: utf-8 -*-
"""
使用稳定的真实玩具图片URL更新商品
使用Pixabay和Pexels的公开图片链接
"""

import re
from pathlib import Path

# 使用Pixabay和Pexels的真实玩具图片URL
# 这些是公开的、稳定的图片链接
REAL_TOY_IMAGE_URLS = {
    "变形金刚": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "玩具枪": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "漫威英雄": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "DC宇宙": [
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    ],
    "毛绒玩具": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "幼儿积木": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "恐龙模型": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
    "拼图益智": [
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    ],
}

def update_with_stable_images():
    """使用稳定的真实图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Pixabay的真实玩具图片
    # 这些是公开的、稳定的CDN链接
    category_urls = {
        "变形金刚": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
            "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
            "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        ],
        "玩具枪": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "漫威英雄": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        ],
        "DC宇宙": [
            "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        ],
        "毛绒玩具": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "幼儿积木": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "恐龙模型": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
        "拼图益智": [
            "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        ],
    }
    
    # 查找所有商品
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"Found {len(matches)} products")
    
    updated_count = 0
    category_counts = {}
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
        index = category_counts[category] - 1
        
        # 获取该分类的图片URL列表
        urls = category_urls.get(category, category_urls["变形金刚"])
        # 循环使用URL，确保每个商品都有图片
        selected_url = urls[index % len(urls)]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 10:
                print(f"[{product_id}] {title} ({category})")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("Using Pixabay CDN - these are real toy photos")
        print("\nPlease clear browser cache (Ctrl+F5) and refresh the page")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Stable Real Toy Images")
    print("=" * 60)
    print("\nUsing Pixabay CDN for real toy photos\n")
    
    update_with_stable_images()
    
    print("\n" + "=" * 60)
    print("Done! Please clear cache (Ctrl+F5) and refresh")
    print("=" * 60)









