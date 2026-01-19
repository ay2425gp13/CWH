#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速更新玩具图片 - 使用公开的图片URL
"""

import re
from pathlib import Path

# 使用Unsplash的公开图片URL（无需API key）
# 这些是真实的玩具相关图片
TOY_IMAGE_URLS = {
    # 变形金刚/机器人玩具
    "transformer": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&auto=format",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    # 玩具枪
    "gun": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 超级英雄
    "superhero": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 毛绒玩具
    "plush": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 积木
    "blocks": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 恐龙
    "dinosaur": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 拼图
    "puzzle": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
}

# 更好的方案：使用Pexels的公开API（无需key，但需要搜索）
# 或者使用一些公开的CDN服务

def get_image_url_by_category(category, index=0):
    """根据分类获取图片URL"""
    category_map = {
        "变形金刚": "transformer",
        "玩具枪": "gun",
        "漫威英雄": "superhero",
        "DC宇宙": "superhero",
        "毛绒玩具": "plush",
        "幼儿积木": "blocks",
        "恐龙模型": "dinosaur",
        "拼图益智": "puzzle"
    }
    
    key = category_map.get(category, "transformer")
    urls = TOY_IMAGE_URLS.get(key, TOY_IMAGE_URLS["transformer"])
    return urls[index % len(urls)]

def update_html_with_real_images():
    """更新HTML文件，使用真实的玩具图片URL"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"错误: 找不到文件 {html_file}")
        return
    
    print("正在读取HTML文件...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Unsplash Source API生成图片URL（根据关键词）
    # 格式: https://source.unsplash.com/featured/280x200/?keyword1,keyword2
    
    category_keywords = {
        "变形金刚": "transformer,robot,action-figure",
        "玩具枪": "toy-gun,nerf,water-gun",
        "漫威英雄": "marvel,superhero,iron-man",
        "DC宇宙": "batman,superman,dc-comics",
        "毛绒玩具": "teddy-bear,plush-toy,stuffed-animal",
        "幼儿积木": "building-blocks,toddler-toys",
        "恐龙模型": "dinosaur,toy-dinosaur",
        "拼图益智": "puzzle,jigsaw,educational"
    }
    
    # 查找所有商品并更新图片URL
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"找到 {len(matches)} 个商品")
    
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
        
        # 获取关键词
        keywords = category_keywords.get(category, "toy")
        
        # 生成Unsplash Source API URL
        # 使用不同的关键词组合来获取不同的图片
        keyword_variations = keywords.split(',')
        selected_keyword = keyword_variations[index % len(keyword_variations)]
        
        new_image_url = f"https://source.unsplash.com/featured/280x200/?{selected_keyword}"
        
        # 查找并替换该商品的图片URL
        # 需要找到该商品对象中的image字段
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            print(f"[OK] [{product_id}] {title} ({category}) -> {selected_keyword}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[SUCCESS] 成功更新 {updated_count} 个商品的图片URL")
        print("\n注意: 这些图片来自Unsplash，首次加载可能需要一些时间")
        print("如果图片无法显示，请检查网络连接或使用本地图片")
    else:
        print("\n未找到需要更新的商品")

if __name__ == "__main__":
    print("=" * 60)
    print("更新商品图片URL")
    print("=" * 60)
    print("\n此脚本将使用Unsplash Source API的图片URL")
    print("图片会根据商品分类自动匹配对应的关键词")
    print("\n开始更新...\n")
    
    update_html_with_real_images()
    
    print("\n" + "=" * 60)
    print("完成！请刷新浏览器查看效果")
    print("=" * 60)


"""
快速更新玩具图片 - 使用公开的图片URL
"""

import re
from pathlib import Path

# 使用Unsplash的公开图片URL（无需API key）
# 这些是真实的玩具相关图片
TOY_IMAGE_URLS = {
    # 变形金刚/机器人玩具
    "transformer": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&auto=format",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop&q=80",
    ],
    # 玩具枪
    "gun": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 超级英雄
    "superhero": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 毛绒玩具
    "plush": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 积木
    "blocks": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 恐龙
    "dinosaur": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    # 拼图
    "puzzle": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
}

# 更好的方案：使用Pexels的公开API（无需key，但需要搜索）
# 或者使用一些公开的CDN服务

def get_image_url_by_category(category, index=0):
    """根据分类获取图片URL"""
    category_map = {
        "变形金刚": "transformer",
        "玩具枪": "gun",
        "漫威英雄": "superhero",
        "DC宇宙": "superhero",
        "毛绒玩具": "plush",
        "幼儿积木": "blocks",
        "恐龙模型": "dinosaur",
        "拼图益智": "puzzle"
    }
    
    key = category_map.get(category, "transformer")
    urls = TOY_IMAGE_URLS.get(key, TOY_IMAGE_URLS["transformer"])
    return urls[index % len(urls)]

def update_html_with_real_images():
    """更新HTML文件，使用真实的玩具图片URL"""
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"错误: 找不到文件 {html_file}")
        return
    
    print("正在读取HTML文件...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用Unsplash Source API生成图片URL（根据关键词）
    # 格式: https://source.unsplash.com/featured/280x200/?keyword1,keyword2
    
    category_keywords = {
        "变形金刚": "transformer,robot,action-figure",
        "玩具枪": "toy-gun,nerf,water-gun",
        "漫威英雄": "marvel,superhero,iron-man",
        "DC宇宙": "batman,superman,dc-comics",
        "毛绒玩具": "teddy-bear,plush-toy,stuffed-animal",
        "幼儿积木": "building-blocks,toddler-toys",
        "恐龙模型": "dinosaur,toy-dinosaur",
        "拼图益智": "puzzle,jigsaw,educational"
    }
    
    # 查找所有商品并更新图片URL
    pattern = r'id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    print(f"找到 {len(matches)} 个商品")
    
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
        
        # 获取关键词
        keywords = category_keywords.get(category, "toy")
        
        # 生成Unsplash Source API URL
        # 使用不同的关键词组合来获取不同的图片
        keyword_variations = keywords.split(',')
        selected_keyword = keyword_variations[index % len(keyword_variations)]
        
        new_image_url = f"https://source.unsplash.com/featured/280x200/?{selected_keyword}"
        
        # 查找并替换该商品的图片URL
        # 需要找到该商品对象中的image字段
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            print(f"[OK] [{product_id}] {title} ({category}) -> {selected_keyword}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[SUCCESS] 成功更新 {updated_count} 个商品的图片URL")
        print("\n注意: 这些图片来自Unsplash，首次加载可能需要一些时间")
        print("如果图片无法显示，请检查网络连接或使用本地图片")
    else:
        print("\n未找到需要更新的商品")

if __name__ == "__main__":
    print("=" * 60)
    print("更新商品图片URL")
    print("=" * 60)
    print("\n此脚本将使用Unsplash Source API的图片URL")
    print("图片会根据商品分类自动匹配对应的关键词")
    print("\n开始更新...\n")
    
    update_html_with_real_images()
    
    print("\n" + "=" * 60)
    print("完成！请刷新浏览器查看效果")
    print("=" * 60)

