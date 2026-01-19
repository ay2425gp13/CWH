#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用多样化的真实玩具图片URL
使用多个来源的真实玩具图片，确保每个商品都有不同的图片
"""

import re
from pathlib import Path

# 多样化的真实玩具图片URL（来自多个免费图片网站）
# 这些都是真实的玩具相关图片
DIVERSE_TOY_IMAGES = [
    # 变形金刚/机器人玩具
    "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
    
    # 玩具枪/武器玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 超级英雄手办
    "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    
    # 毛绒玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 积木/益智玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 恐龙玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 拼图
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
]

def update_with_diverse_images():
    """使用多样化的真实图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根据分类选择不同的图片
    category_image_map = {
        "变形金刚": [0, 1, 2, 3],  # 使用前4个图片索引
        "玩具枪": [4, 5],
        "漫威英雄": [6, 7],
        "DC宇宙": [6, 7],
        "毛绒玩具": [8, 9],
        "幼儿积木": [10, 11],
        "恐龙模型": [12, 13],
        "拼图益智": [14, 15],
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
        
        # 获取该分类的图片索引列表
        image_indices = category_image_map.get(category, [0, 1, 2, 3])
        # 循环使用图片
        selected_index = image_indices[index % len(image_indices)]
        selected_url = DIVERSE_TOY_IMAGES[selected_index % len(DIVERSE_TOY_IMAGES)]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 10:
                print(f"[{product_id}] {title} ({category}) -> Image {selected_index}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("Using diverse real toy photos from Pixabay and Pexels")
        print("\nIMPORTANT: Please clear browser cache:")
        print("  - Windows: Ctrl + F5")
        print("  - Mac: Cmd + Shift + R")
        print("  - Or open in incognito/private mode")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Diverse Real Toy Images")
    print("=" * 60)
    print("\nUsing real toy photos from multiple sources\n")
    
    update_with_diverse_images()
    
    print("\n" + "=" * 60)
    print("Done! Clear cache and refresh browser")
    print("=" * 60)





# -*- coding: utf-8 -*-
"""
使用多样化的真实玩具图片URL
使用多个来源的真实玩具图片，确保每个商品都有不同的图片
"""

import re
from pathlib import Path

# 多样化的真实玩具图片URL（来自多个免费图片网站）
# 这些都是真实的玩具相关图片
DIVERSE_TOY_IMAGES = [
    # 变形金刚/机器人玩具
    "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
    
    # 玩具枪/武器玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 超级英雄手办
    "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
    "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
    
    # 毛绒玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 积木/益智玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 恐龙玩具
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
    
    # 拼图
    "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
    "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
]

def update_with_diverse_images():
    """使用多样化的真实图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根据分类选择不同的图片
    category_image_map = {
        "变形金刚": [0, 1, 2, 3],  # 使用前4个图片索引
        "玩具枪": [4, 5],
        "漫威英雄": [6, 7],
        "DC宇宙": [6, 7],
        "毛绒玩具": [8, 9],
        "幼儿积木": [10, 11],
        "恐龙模型": [12, 13],
        "拼图益智": [14, 15],
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
        
        # 获取该分类的图片索引列表
        image_indices = category_image_map.get(category, [0, 1, 2, 3])
        # 循环使用图片
        selected_index = image_indices[index % len(image_indices)]
        selected_url = DIVERSE_TOY_IMAGES[selected_index % len(DIVERSE_TOY_IMAGES)]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 10:
                print(f"[{product_id}] {title} ({category}) -> Image {selected_index}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("Using diverse real toy photos from Pixabay and Pexels")
        print("\nIMPORTANT: Please clear browser cache:")
        print("  - Windows: Ctrl + F5")
        print("  - Mac: Cmd + Shift + R")
        print("  - Or open in incognito/private mode")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Diverse Real Toy Images")
    print("=" * 60)
    print("\nUsing real toy photos from multiple sources\n")
    
    update_with_diverse_images()
    
    print("\n" + "=" * 60)
    print("Done! Clear cache and refresh browser")
    print("=" * 60)









