#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩具图片下载脚本
支持从多个来源获取玩具图片：
1. Unsplash API (需要API key)
2. Pexels API (需要API key)
3. 公开的CDN图片URL
4. 本地图片文件
"""

import os
import json
import requests
from pathlib import Path
import time

# 配置
IMAGES_DIR = Path("frontend/images/toys")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 商品分类对应的图片搜索关键词
CATEGORY_KEYWORDS = {
    "变形金刚": ["transformer", "optimus prime", "action figure", "robot toy"],
    "玩具枪": ["toy gun", "nerf gun", "water gun", "toy weapon"],
    "漫威英雄": ["marvel action figure", "iron man", "spider man", "superhero toy"],
    "DC宇宙": ["batman toy", "superman", "dc action figure", "superhero"],
    "毛绒玩具": ["teddy bear", "plush toy", "stuffed animal", "soft toy"],
    "幼儿积木": ["baby blocks", "building blocks", "toddler toys", "educational toys"],
    "恐龙模型": ["dinosaur toy", "dino figure", "prehistoric toy"],
    "拼图益智": ["puzzle", "jigsaw puzzle", "educational puzzle"]
}

# 使用Unsplash Source API (无需API key，但有限制)
UNSPLASH_SOURCE = "https://source.unsplash.com/featured/280x200"

# 备用的公开图片CDN (示例)
BACKUP_IMAGE_URLS = {
    "变形金刚": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "玩具枪": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "漫威英雄": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "毛绒玩具": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
}

def download_image(url, filepath, max_retries=3):
    """下载图片到本地"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ 下载成功: {filepath.name}")
            return True
        except Exception as e:
            print(f"✗ 下载失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False

def get_unsplash_image_url(keyword, width=280, height=200):
    """获取Unsplash图片URL (使用Source API，无需key)"""
    # 使用Unsplash Source API
    return f"https://source.unsplash.com/featured/{width}x{height}/?{keyword.replace(' ', ',')}"

def update_product_images():
    """更新商品数据中的图片路径"""
    # 读取现有的商品数据
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"错误: 找不到文件 {html_file}")
        return
    
    print("正在读取商品数据...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取productsData数组
    import re
    pattern = r'const productsData = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("错误: 无法找到productsData数组")
        return
    
    products_data_str = match.group(1)
    
    # 解析JSON (需要手动处理，因为可能有注释)
    # 这里我们直接替换图片URL
    print("\n开始更新图片路径...")
    
    # 统计需要更新的商品
    product_count = content.count('image: "https://via.placeholder.com')
    print(f"找到 {product_count} 个需要更新图片的商品")
    
    # 为每个商品生成新的图片路径
    updated_content = content
    product_id = 1
    
    # 按分类更新图片
    current_category = None
    category_index = {}
    
    for line in content.split('\n'):
        if 'category:' in line:
            # 提取分类
            cat_match = re.search(r'category:\s*"([^"]+)"', line)
            if cat_match:
                current_category = cat_match.group(1)
                if current_category not in category_index:
                    category_index[current_category] = 0
                category_index[current_category] += 1
    
    print(f"\n检测到以下分类: {list(category_index.keys())}")
    
    return updated_content

def generate_image_mapping():
    """生成商品ID到图片文件的映射"""
    mapping = {}
    
    # 读取HTML文件，提取商品信息
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取商品数据
    import re
    pattern = r'{\s*id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for product_id, title, category in matches:
        product_id = int(product_id)
        # 生成图片文件名
        image_filename = f"toy_{product_id:03d}.jpg"
        image_path = f"images/toys/{image_filename}"
        mapping[product_id] = {
            'title': title,
            'category': category,
            'image_path': image_path,
            'filename': image_filename
        }
    
    return mapping

def main():
    print("=" * 60)
    print("玩具图片下载工具")
    print("=" * 60)
    print("\n选项:")
    print("1. 使用Unsplash Source API下载图片 (免费，无需API key)")
    print("2. 使用本地图片文件 (需要手动将图片放入 frontend/images/toys/)")
    print("3. 生成图片映射文件")
    print("4. 更新HTML中的图片路径")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        print("\n使用Unsplash Source API下载图片...")
        mapping = generate_image_mapping()
        
        for product_id, info in mapping.items():
            category = info['category']
            keyword = CATEGORY_KEYWORDS.get(category, ["toy"])[0]
            
            # 获取图片URL
            image_url = get_unsplash_image_url(keyword)
            filepath = IMAGES_DIR / info['filename']
            
            print(f"\n[{product_id}] {info['title']} ({category})")
            print(f"  下载: {image_url}")
            
            if download_image(image_url, filepath):
                # 更新HTML中的图片路径
                update_html_image_path(product_id, f"images/toys/{info['filename']}")
            
            time.sleep(1)  # 避免请求过快
        
        print("\n✓ 所有图片下载完成!")
        
    elif choice == "2":
        print("\n使用本地图片文件...")
        print(f"请将图片文件放入: {IMAGES_DIR.absolute()}")
        print("图片命名格式: toy_001.jpg, toy_002.jpg, ...")
        
        # 检查已存在的图片
        existing_images = list(IMAGES_DIR.glob("toy_*.jpg"))
        if existing_images:
            print(f"\n找到 {len(existing_images)} 个图片文件")
            for img in sorted(existing_images):
                print(f"  - {img.name}")
        else:
            print("\n未找到图片文件")
    
    elif choice == "3":
        print("\n生成图片映射...")
        mapping = generate_image_mapping()
        
        mapping_file = Path("image_mapping.json")
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 映射文件已保存: {mapping_file}")
        print(f"  共 {len(mapping)} 个商品")
    
    elif choice == "4":
        print("\n更新HTML中的图片路径...")
        update_all_image_paths()
        print("✓ 更新完成!")
    
    else:
        print("无效的选择")

def update_html_image_path(product_id, new_path):
    """更新HTML中指定商品的图片路径"""
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换
    pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
    replacement = rf'\1{new_path}\2'
    content = re.sub(pattern, replacement, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def update_all_image_paths():
    """批量更新所有商品的图片路径"""
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有商品
    import re
    pattern = r'id:\s*(\d+),.*?image:\s*"([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)
    
    updated_count = 0
    for product_id, old_path in matches:
        product_id = int(product_id)
        new_path = f"images/toys/toy_{product_id:03d}.jpg"
        
        # 检查图片文件是否存在
        image_file = Path(f"frontend/{new_path}")
        if image_file.exists():
            # 替换路径
            old_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
            new_replacement = rf'\1{new_path}\2'
            content = re.sub(old_pattern, new_replacement, content)
            updated_count += 1
            print(f"✓ 更新商品 {product_id}: {new_path}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ 共更新 {updated_count} 个商品的图片路径")
    else:
        print("\n未找到可更新的图片")

if __name__ == "__main__":
    import re
    main()





# -*- coding: utf-8 -*-
"""
玩具图片下载脚本
支持从多个来源获取玩具图片：
1. Unsplash API (需要API key)
2. Pexels API (需要API key)
3. 公开的CDN图片URL
4. 本地图片文件
"""

import os
import json
import requests
from pathlib import Path
import time

# 配置
IMAGES_DIR = Path("frontend/images/toys")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 商品分类对应的图片搜索关键词
CATEGORY_KEYWORDS = {
    "变形金刚": ["transformer", "optimus prime", "action figure", "robot toy"],
    "玩具枪": ["toy gun", "nerf gun", "water gun", "toy weapon"],
    "漫威英雄": ["marvel action figure", "iron man", "spider man", "superhero toy"],
    "DC宇宙": ["batman toy", "superman", "dc action figure", "superhero"],
    "毛绒玩具": ["teddy bear", "plush toy", "stuffed animal", "soft toy"],
    "幼儿积木": ["baby blocks", "building blocks", "toddler toys", "educational toys"],
    "恐龙模型": ["dinosaur toy", "dino figure", "prehistoric toy"],
    "拼图益智": ["puzzle", "jigsaw puzzle", "educational puzzle"]
}

# 使用Unsplash Source API (无需API key，但有限制)
UNSPLASH_SOURCE = "https://source.unsplash.com/featured/280x200"

# 备用的公开图片CDN (示例)
BACKUP_IMAGE_URLS = {
    "变形金刚": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "玩具枪": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "漫威英雄": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
    "毛绒玩具": [
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=280&h=200&fit=crop",
    ],
}

def download_image(url, filepath, max_retries=3):
    """下载图片到本地"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ 下载成功: {filepath.name}")
            return True
        except Exception as e:
            print(f"✗ 下载失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return False

def get_unsplash_image_url(keyword, width=280, height=200):
    """获取Unsplash图片URL (使用Source API，无需key)"""
    # 使用Unsplash Source API
    return f"https://source.unsplash.com/featured/{width}x{height}/?{keyword.replace(' ', ',')}"

def update_product_images():
    """更新商品数据中的图片路径"""
    # 读取现有的商品数据
    html_file = Path("frontend/platform-market.html")
    
    if not html_file.exists():
        print(f"错误: 找不到文件 {html_file}")
        return
    
    print("正在读取商品数据...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取productsData数组
    import re
    pattern = r'const productsData = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("错误: 无法找到productsData数组")
        return
    
    products_data_str = match.group(1)
    
    # 解析JSON (需要手动处理，因为可能有注释)
    # 这里我们直接替换图片URL
    print("\n开始更新图片路径...")
    
    # 统计需要更新的商品
    product_count = content.count('image: "https://via.placeholder.com')
    print(f"找到 {product_count} 个需要更新图片的商品")
    
    # 为每个商品生成新的图片路径
    updated_content = content
    product_id = 1
    
    # 按分类更新图片
    current_category = None
    category_index = {}
    
    for line in content.split('\n'):
        if 'category:' in line:
            # 提取分类
            cat_match = re.search(r'category:\s*"([^"]+)"', line)
            if cat_match:
                current_category = cat_match.group(1)
                if current_category not in category_index:
                    category_index[current_category] = 0
                category_index[current_category] += 1
    
    print(f"\n检测到以下分类: {list(category_index.keys())}")
    
    return updated_content

def generate_image_mapping():
    """生成商品ID到图片文件的映射"""
    mapping = {}
    
    # 读取HTML文件，提取商品信息
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取商品数据
    import re
    pattern = r'{\s*id:\s*(\d+),.*?title:\s*"([^"]+)",.*?category:\s*"([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for product_id, title, category in matches:
        product_id = int(product_id)
        # 生成图片文件名
        image_filename = f"toy_{product_id:03d}.jpg"
        image_path = f"images/toys/{image_filename}"
        mapping[product_id] = {
            'title': title,
            'category': category,
            'image_path': image_path,
            'filename': image_filename
        }
    
    return mapping

def main():
    print("=" * 60)
    print("玩具图片下载工具")
    print("=" * 60)
    print("\n选项:")
    print("1. 使用Unsplash Source API下载图片 (免费，无需API key)")
    print("2. 使用本地图片文件 (需要手动将图片放入 frontend/images/toys/)")
    print("3. 生成图片映射文件")
    print("4. 更新HTML中的图片路径")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        print("\n使用Unsplash Source API下载图片...")
        mapping = generate_image_mapping()
        
        for product_id, info in mapping.items():
            category = info['category']
            keyword = CATEGORY_KEYWORDS.get(category, ["toy"])[0]
            
            # 获取图片URL
            image_url = get_unsplash_image_url(keyword)
            filepath = IMAGES_DIR / info['filename']
            
            print(f"\n[{product_id}] {info['title']} ({category})")
            print(f"  下载: {image_url}")
            
            if download_image(image_url, filepath):
                # 更新HTML中的图片路径
                update_html_image_path(product_id, f"images/toys/{info['filename']}")
            
            time.sleep(1)  # 避免请求过快
        
        print("\n✓ 所有图片下载完成!")
        
    elif choice == "2":
        print("\n使用本地图片文件...")
        print(f"请将图片文件放入: {IMAGES_DIR.absolute()}")
        print("图片命名格式: toy_001.jpg, toy_002.jpg, ...")
        
        # 检查已存在的图片
        existing_images = list(IMAGES_DIR.glob("toy_*.jpg"))
        if existing_images:
            print(f"\n找到 {len(existing_images)} 个图片文件")
            for img in sorted(existing_images):
                print(f"  - {img.name}")
        else:
            print("\n未找到图片文件")
    
    elif choice == "3":
        print("\n生成图片映射...")
        mapping = generate_image_mapping()
        
        mapping_file = Path("image_mapping.json")
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 映射文件已保存: {mapping_file}")
        print(f"  共 {len(mapping)} 个商品")
    
    elif choice == "4":
        print("\n更新HTML中的图片路径...")
        update_all_image_paths()
        print("✓ 更新完成!")
    
    else:
        print("无效的选择")

def update_html_image_path(product_id, new_path):
    """更新HTML中指定商品的图片路径"""
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换
    pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
    replacement = rf'\1{new_path}\2'
    content = re.sub(pattern, replacement, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def update_all_image_paths():
    """批量更新所有商品的图片路径"""
    html_file = Path("frontend/platform-market.html")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有商品
    import re
    pattern = r'id:\s*(\d+),.*?image:\s*"([^"]+)"'
    matches = re.findall(pattern, content, re.DOTALL)
    
    updated_count = 0
    for product_id, old_path in matches:
        product_id = int(product_id)
        new_path = f"images/toys/toy_{product_id:03d}.jpg"
        
        # 检查图片文件是否存在
        image_file = Path(f"frontend/{new_path}")
        if image_file.exists():
            # 替换路径
            old_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
            new_replacement = rf'\1{new_path}\2'
            content = re.sub(old_pattern, new_replacement, content)
            updated_count += 1
            print(f"✓ 更新商品 {product_id}: {new_path}")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ 共更新 {updated_count} 个商品的图片路径")
    else:
        print("\n未找到可更新的图片")

if __name__ == "__main__":
    import re
    main()









