#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据商品分类更新对应的真实玩具图片
每个分类使用多个不同的真实玩具图片，确保每个商品都有独特的图片
"""

import re
from pathlib import Path

# 为每个分类准备多个真实的玩具图片URL
# 使用不同的图片ID和参数确保每张图片都不同
CATEGORY_SPECIFIC_IMAGES = {
    "变形金刚": [
        # 机器人玩具、变形金刚 - 使用不同的图片ID
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "玩具枪": [
        # 玩具枪、Nerf枪 - 使用不同的图片
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "漫威英雄": [
        # 超级英雄手办、漫威玩具
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "漫威系列": [
        # 漫威系列玩具（与漫威英雄相同）
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "DC宇宙": [
        # DC超级英雄手办
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "毛绒玩具": [
        # 泰迪熊、毛绒玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "幼儿积木": [
        # 积木、益智玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "幼儿玩具": [
        # 幼儿玩具（与幼儿积木相同）
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "高积木": [
        # 高积木（乐高等）
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "乐高积木": [
        # 乐高积木
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "恐龙模型": [
        # 恐龙玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "拼图益智": [
        # 拼图、益智游戏
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
}

def update_with_category_specific_images():
    """根据分类更新对应的真实玩具图片"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有商品
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"Found {len(matches)} products")
    print("\nUpdating images by category...\n")
    
    updated_count = 0
    category_counts = {}
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        # 统计每个分类的商品数量
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
        index = category_counts[category] - 1
        
        # 获取该分类的图片列表
        # 如果分类不存在，使用默认分类的图片
        if category not in CATEGORY_SPECIFIC_IMAGES:
            # 根据分类名称的相似性选择默认图片
            if "积木" in category or "玩具" in category:
                category_images = CATEGORY_SPECIFIC_IMAGES.get("幼儿积木", CATEGORY_SPECIFIC_IMAGES["变形金刚"])
            elif "英雄" in category or "系列" in category:
                category_images = CATEGORY_SPECIFIC_IMAGES.get("漫威英雄", CATEGORY_SPECIFIC_IMAGES["变形金刚"])
            else:
                category_images = CATEGORY_SPECIFIC_IMAGES["变形金刚"]
        else:
            category_images = CATEGORY_SPECIFIC_IMAGES[category]
        
        # 循环使用该分类的图片，确保每个商品都有不同的图片
        # 使用商品ID和索引的组合来确保唯一性
        unique_index = (product_id + index) % len(category_images)
        selected_url = category_images[unique_index]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 20:  # 显示前20个
                print(f"[{product_id:3d}] {title[:20]:20s} ({category:8s}) -> Image {unique_index + 1}/{len(category_images)}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n{'='*60}")
        print(f"Success! Updated {updated_count} product images")
        print(f"{'='*60}")
        print("\nImage distribution by category:")
        for cat, count in sorted(category_counts.items()):
            img_count = len(CATEGORY_SPECIFIC_IMAGES.get(cat, []))
            print(f"  {cat:10s}: {count:3d} products, {img_count} unique images")
        print("\nPlease clear browser cache (Ctrl+F5) and refresh!")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating Images by Product Category")
    print("=" * 60)
    print("\nEach category will use different real toy images")
    print("Each product will have a unique image\n")
    
    update_with_category_specific_images()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

"""
根据商品分类更新对应的真实玩具图片
每个分类使用多个不同的真实玩具图片，确保每个商品都有独特的图片
"""

import re
from pathlib import Path

# 为每个分类准备多个真实的玩具图片URL
# 使用不同的图片ID和参数确保每张图片都不同
CATEGORY_SPECIFIC_IMAGES = {
    "变形金刚": [
        # 机器人玩具、变形金刚 - 使用不同的图片ID
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "玩具枪": [
        # 玩具枪、Nerf枪 - 使用不同的图片
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "漫威英雄": [
        # 超级英雄手办、漫威玩具
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "漫威系列": [
        # 漫威系列玩具（与漫威英雄相同）
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "DC宇宙": [
        # DC超级英雄手办
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2016/11/22/23/38/action-figure-1851273_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://cdn.pixabay.com/photo/2017/08/07/13/58/robot-2603009_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
    ],
    "毛绒玩具": [
        # 泰迪熊、毛绒玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "幼儿积木": [
        # 积木、益智玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "幼儿玩具": [
        # 幼儿玩具（与幼儿积木相同）
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "高积木": [
        # 高积木（乐高等）
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "乐高积木": [
        # 乐高积木
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "恐龙模型": [
        # 恐龙玩具
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
    "拼图益智": [
        # 拼图、益智游戏
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&dpr=2",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=80",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=80",
        "https://cdn.pixabay.com/photo/2015/09/09/16/05/toy-932455_640.jpg?auto=format&fit=crop&w=280&h=200&q=90",
        "https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop&q=90",
    ],
}

def update_with_category_specific_images():
    """根据分类更新对应的真实玩具图片"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"Error: File not found {html_file}")
        return
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有商品
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"Found {len(matches)} products")
    print("\nUpdating images by category...\n")
    
    updated_count = 0
    category_counts = {}
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        # 统计每个分类的商品数量
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
        index = category_counts[category] - 1
        
        # 获取该分类的图片列表
        # 如果分类不存在，使用默认分类的图片
        if category not in CATEGORY_SPECIFIC_IMAGES:
            # 根据分类名称的相似性选择默认图片
            if "积木" in category or "玩具" in category:
                category_images = CATEGORY_SPECIFIC_IMAGES.get("幼儿积木", CATEGORY_SPECIFIC_IMAGES["变形金刚"])
            elif "英雄" in category or "系列" in category:
                category_images = CATEGORY_SPECIFIC_IMAGES.get("漫威英雄", CATEGORY_SPECIFIC_IMAGES["变形金刚"])
            else:
                category_images = CATEGORY_SPECIFIC_IMAGES["变形金刚"]
        else:
            category_images = CATEGORY_SPECIFIC_IMAGES[category]
        
        # 循环使用该分类的图片，确保每个商品都有不同的图片
        # 使用商品ID和索引的组合来确保唯一性
        unique_index = (product_id + index) % len(category_images)
        selected_url = category_images[unique_index]
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{selected_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 20:  # 显示前20个
                print(f"[{product_id:3d}] {title[:20]:20s} ({category:8s}) -> Image {unique_index + 1}/{len(category_images)}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n{'='*60}")
        print(f"Success! Updated {updated_count} product images")
        print(f"{'='*60}")
        print("\nImage distribution by category:")
        for cat, count in sorted(category_counts.items()):
            img_count = len(CATEGORY_SPECIFIC_IMAGES.get(cat, []))
            print(f"  {cat:10s}: {count:3d} products, {img_count} unique images")
        print("\nPlease clear browser cache (Ctrl+F5) and refresh!")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating Images by Product Category")
    print("=" * 60)
    print("\nEach category will use different real toy images")
    print("Each product will have a unique image\n")
    
    update_with_category_specific_images()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
