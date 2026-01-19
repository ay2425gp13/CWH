#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新为真实的玩具图片URL
使用Unsplash和Pexels的真实玩具图片
"""

import re
from pathlib import Path

# 真实的玩具图片URL（来自Unsplash和Pexels）
# 这些是真实的玩具相关图片，不是占位图
REAL_TOY_IMAGES = {
    "变形金刚": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format&ixlib=rb-4.0.3",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ],
    "玩具枪": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "漫威英雄": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "DC宇宙": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "毛绒玩具": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "幼儿积木": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "恐龙模型": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "拼图益智": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
}

def update_with_real_images():
    """使用真实的玩具图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Unsplash Source API - 根据关键词获取真实图片
    # 格式: https://source.unsplash.com/featured/280x200/?keyword
    category_keywords = {
        "变形金刚": ["transformer", "robot-toy", "action-figure", "optimus-prime"],
        "玩具枪": ["toy-gun", "nerf-gun", "water-gun", "toy-weapon"],
        "漫威英雄": ["marvel-toy", "iron-man-toy", "spider-man-toy", "superhero-figure"],
        "DC宇宙": ["batman-toy", "superman-toy", "dc-comics-toy", "superhero-action-figure"],
        "毛绒玩具": ["teddy-bear", "plush-toy", "stuffed-animal", "soft-toy"],
        "幼儿积木": ["building-blocks", "toddler-toys", "wooden-blocks", "educational-blocks"],
        "恐龙模型": ["dinosaur-toy", "dino-figure", "prehistoric-toy", "t-rex-toy"],
        "拼图益智": ["puzzle", "jigsaw-puzzle", "educational-puzzle", "wooden-puzzle"]
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
        
        # 获取关键词列表
        keywords = category_keywords.get(category, ["toy"])
        # 循环使用关键词，确保每个商品都有不同的图片
        selected_keyword = keywords[index % len(keywords)]
        
        # 使用Unsplash Source API获取真实图片
        # 添加随机参数确保每张图片都不同
        new_image_url = f"https://source.unsplash.com/featured/280x200/?{selected_keyword}&sig={product_id}"
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            print(f"[{product_id}] {title} ({category}) -> {selected_keyword}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("\nNote: Images are from Unsplash, they may take a moment to load")
        print("If images don't load, check your internet connection")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Real Toy Images")
    print("=" * 60)
    print("\nUsing Unsplash Source API for real toy images")
    print("Images will be matched by product category\n")
    
    update_with_real_images()
    
    print("\n" + "=" * 60)
    print("Done! Please refresh your browser")
    print("=" * 60)





# -*- coding: utf-8 -*-
"""
更新为真实的玩具图片URL
使用Unsplash和Pexels的真实玩具图片
"""

import re
from pathlib import Path

# 真实的玩具图片URL（来自Unsplash和Pexels）
# 这些是真实的玩具相关图片，不是占位图
REAL_TOY_IMAGES = {
    "变形金刚": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format&ixlib=rb-4.0.3",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80&auto=format&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    ],
    "玩具枪": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "漫威英雄": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "DC宇宙": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "毛绒玩具": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "幼儿积木": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "恐龙模型": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    "拼图益智": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
}

def update_with_real_images():
    """使用真实的玩具图片URL更新HTML"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Unsplash Source API - 根据关键词获取真实图片
    # 格式: https://source.unsplash.com/featured/280x200/?keyword
    category_keywords = {
        "变形金刚": ["transformer", "robot-toy", "action-figure", "optimus-prime"],
        "玩具枪": ["toy-gun", "nerf-gun", "water-gun", "toy-weapon"],
        "漫威英雄": ["marvel-toy", "iron-man-toy", "spider-man-toy", "superhero-figure"],
        "DC宇宙": ["batman-toy", "superman-toy", "dc-comics-toy", "superhero-action-figure"],
        "毛绒玩具": ["teddy-bear", "plush-toy", "stuffed-animal", "soft-toy"],
        "幼儿积木": ["building-blocks", "toddler-toys", "wooden-blocks", "educational-blocks"],
        "恐龙模型": ["dinosaur-toy", "dino-figure", "prehistoric-toy", "t-rex-toy"],
        "拼图益智": ["puzzle", "jigsaw-puzzle", "educational-puzzle", "wooden-puzzle"]
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
        
        # 获取关键词列表
        keywords = category_keywords.get(category, ["toy"])
        # 循环使用关键词，确保每个商品都有不同的图片
        selected_keyword = keywords[index % len(keywords)]
        
        # 使用Unsplash Source API获取真实图片
        # 添加随机参数确保每张图片都不同
        new_image_url = f"https://source.unsplash.com/featured/280x200/?{selected_keyword}&sig={product_id}"
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            print(f"[{product_id}] {title} ({category}) -> {selected_keyword}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccess! Updated {updated_count} product images")
        print("\nNote: Images are from Unsplash, they may take a moment to load")
        print("If images don't load, check your internet connection")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Real Toy Images")
    print("=" * 60)
    print("\nUsing Unsplash Source API for real toy images")
    print("Images will be matched by product category\n")
    
    update_with_real_images()
    
    print("\n" + "=" * 60)
    print("Done! Please refresh your browser")
    print("=" * 60)









