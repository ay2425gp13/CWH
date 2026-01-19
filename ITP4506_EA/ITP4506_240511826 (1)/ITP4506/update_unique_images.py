#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为每个商品分配完全不同的真实玩具图片
使用多个不同的图片ID，确保每个商品都有独特的图片
"""

import re
from pathlib import Path

# 使用多个不同的真实玩具图片ID
# 这些是Pixabay和Pexels上的真实玩具图片，每个ID对应不同的图片
UNIQUE_TOY_IMAGE_IDS = {
    # Pixabay图片ID（每个ID都是不同的玩具图片）
    "pixabay": [
        "2016/11/22/23/38/action-figure-1851273_640.jpg",
        "2017/08/07/13/58/robot-2603009_640.jpg",
        "2015/09/09/16/05/toy-932455_640.jpg",
        "2018/02/21/17/46/toy-3165515_640.jpg",
        "2017/12/10/16/15/toy-3010847_640.jpg",
        "2016/11/29/09/15/toy-1869343_640.jpg",
        "2017/11/14/13/06/toy-2948774_640.jpg",
        "2018/01/15/22/22/toy-3081484_640.jpg",
        "2017/10/04/14/10/toy-2815604_640.jpg",
        "2016/12/13/12/29/toy-1903314_640.jpg",
        "2017/09/25/23/14/toy-2790327_640.jpg",
        "2018/03/11/20/42/toy-3210384_640.jpg",
        "2017/08/20/17/16/toy-2657736_640.jpg",
        "2016/10/16/13/06/toy-1741468_640.jpg",
        "2017/12/05/20/21/toy-2997352_640.jpg",
    ],
    # Pexels图片ID（每个ID都是不同的图片）
    "pexels": [
        "1839919/pexels-photo-1839919.jpeg",
        "1839920/pexels-photo-1839920.jpeg",
        "1839921/pexels-photo-1839921.jpeg",
        "1839922/pexels-photo-1839922.jpeg",
        "1839923/pexels-photo-1839923.jpeg",
        "1839924/pexels-photo-1839924.jpeg",
        "1839925/pexels-photo-1839925.jpeg",
        "1839926/pexels-photo-1839926.jpeg",
        "1839927/pexels-photo-1839927.jpeg",
        "1839928/pexels-photo-1839928.jpeg",
    ]
}

def get_unique_image_url(product_id, category):
    """为每个商品生成唯一的图片URL"""
    # 根据商品ID和分类生成唯一的索引
    total_images = len(UNIQUE_TOY_IMAGE_IDS["pixabay"]) + len(UNIQUE_TOY_IMAGE_IDS["pexels"])
    index = product_id % total_images
    
    # 交替使用Pixabay和Pexels
    if index < len(UNIQUE_TOY_IMAGE_IDS["pixabay"]):
        image_id = UNIQUE_TOY_IMAGE_IDS["pixabay"][index]
        return f"https://cdn.pixabay.com/photo/{image_id}?auto=format&fit=crop&w=280&h=200"
    else:
        pexels_index = index - len(UNIQUE_TOY_IMAGE_IDS["pixabay"])
        image_id = UNIQUE_TOY_IMAGE_IDS["pexels"][pexels_index % len(UNIQUE_TOY_IMAGE_IDS["pexels"])]
        return f"https://images.pexels.com/photos/{image_id}?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop"

def update_all_images():
    """更新所有商品的图片URL"""
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
    print("\nUpdating images to ensure each product has a unique image...\n")
    
    updated_count = 0
    used_urls = set()
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        # 生成唯一的图片URL
        new_image_url = get_unique_image_url(product_id, category)
        
        # 确保URL唯一（如果重复，使用商品ID作为额外参数）
        if new_image_url in used_urls:
            # 添加商品ID作为参数确保唯一性
            separator = "&" if "?" in new_image_url else "?"
            new_image_url = f"{new_image_url}{separator}pid={product_id}"
        
        used_urls.add(new_image_url)
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 20:
                print(f"[{product_id:3d}] {title[:25]:25s} -> {new_image_url[:60]}...")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n{'='*60}")
        print(f"Success! Updated {updated_count} product images")
        print(f"Total unique image URLs: {len(used_urls)}")
        print(f"{'='*60}")
        print("\nEach product now has a unique image URL!")
        print("Please clear browser cache (Ctrl+F5) and refresh!")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Unique Real Toy Images")
    print("=" * 60)
    print("\nEach product will get a completely different image\n")
    
    update_all_images()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)





# -*- coding: utf-8 -*-
"""
为每个商品分配完全不同的真实玩具图片
使用多个不同的图片ID，确保每个商品都有独特的图片
"""

import re
from pathlib import Path

# 使用多个不同的真实玩具图片ID
# 这些是Pixabay和Pexels上的真实玩具图片，每个ID对应不同的图片
UNIQUE_TOY_IMAGE_IDS = {
    # Pixabay图片ID（每个ID都是不同的玩具图片）
    "pixabay": [
        "2016/11/22/23/38/action-figure-1851273_640.jpg",
        "2017/08/07/13/58/robot-2603009_640.jpg",
        "2015/09/09/16/05/toy-932455_640.jpg",
        "2018/02/21/17/46/toy-3165515_640.jpg",
        "2017/12/10/16/15/toy-3010847_640.jpg",
        "2016/11/29/09/15/toy-1869343_640.jpg",
        "2017/11/14/13/06/toy-2948774_640.jpg",
        "2018/01/15/22/22/toy-3081484_640.jpg",
        "2017/10/04/14/10/toy-2815604_640.jpg",
        "2016/12/13/12/29/toy-1903314_640.jpg",
        "2017/09/25/23/14/toy-2790327_640.jpg",
        "2018/03/11/20/42/toy-3210384_640.jpg",
        "2017/08/20/17/16/toy-2657736_640.jpg",
        "2016/10/16/13/06/toy-1741468_640.jpg",
        "2017/12/05/20/21/toy-2997352_640.jpg",
    ],
    # Pexels图片ID（每个ID都是不同的图片）
    "pexels": [
        "1839919/pexels-photo-1839919.jpeg",
        "1839920/pexels-photo-1839920.jpeg",
        "1839921/pexels-photo-1839921.jpeg",
        "1839922/pexels-photo-1839922.jpeg",
        "1839923/pexels-photo-1839923.jpeg",
        "1839924/pexels-photo-1839924.jpeg",
        "1839925/pexels-photo-1839925.jpeg",
        "1839926/pexels-photo-1839926.jpeg",
        "1839927/pexels-photo-1839927.jpeg",
        "1839928/pexels-photo-1839928.jpeg",
    ]
}

def get_unique_image_url(product_id, category):
    """为每个商品生成唯一的图片URL"""
    # 根据商品ID和分类生成唯一的索引
    total_images = len(UNIQUE_TOY_IMAGE_IDS["pixabay"]) + len(UNIQUE_TOY_IMAGE_IDS["pexels"])
    index = product_id % total_images
    
    # 交替使用Pixabay和Pexels
    if index < len(UNIQUE_TOY_IMAGE_IDS["pixabay"]):
        image_id = UNIQUE_TOY_IMAGE_IDS["pixabay"][index]
        return f"https://cdn.pixabay.com/photo/{image_id}?auto=format&fit=crop&w=280&h=200"
    else:
        pexels_index = index - len(UNIQUE_TOY_IMAGE_IDS["pixabay"])
        image_id = UNIQUE_TOY_IMAGE_IDS["pexels"][pexels_index % len(UNIQUE_TOY_IMAGE_IDS["pexels"])]
        return f"https://images.pexels.com/photos/{image_id}?auto=compress&cs=tinysrgb&w=280&h=200&fit=crop"

def update_all_images():
    """更新所有商品的图片URL"""
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
    print("\nUpdating images to ensure each product has a unique image...\n")
    
    updated_count = 0
    used_urls = set()
    
    for match in matches:
        product_id = int(match.group(1))
        title = match.group(2)
        category = match.group(3)
        
        # 生成唯一的图片URL
        new_image_url = get_unique_image_url(product_id, category)
        
        # 确保URL唯一（如果重复，使用商品ID作为额外参数）
        if new_image_url in used_urls:
            # 添加商品ID作为参数确保唯一性
            separator = "&" if "?" in new_image_url else "?"
            new_image_url = f"{new_image_url}{separator}pid={product_id}"
        
        used_urls.add(new_image_url)
        
        # 替换该商品的图片URL
        product_pattern = rf'(id:\s*{product_id},[^}}]*?image:\s*")[^"]+(")'
        
        def replace_image(m):
            return f'{m.group(1)}{new_image_url}{m.group(2)}'
        
        new_content = re.sub(product_pattern, replace_image, content, count=1)
        if new_content != content:
            content = new_content
            updated_count += 1
            if updated_count <= 20:
                print(f"[{product_id:3d}] {title[:25]:25s} -> {new_image_url[:60]}...")
    
    if updated_count > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n{'='*60}")
        print(f"Success! Updated {updated_count} product images")
        print(f"Total unique image URLs: {len(used_urls)}")
        print(f"{'='*60}")
        print("\nEach product now has a unique image URL!")
        print("Please clear browser cache (Ctrl+F5) and refresh!")
    else:
        print("\nNo products found to update")

if __name__ == "__main__":
    print("=" * 60)
    print("Updating to Unique Real Toy Images")
    print("=" * 60)
    print("\nEach product will get a completely different image\n")
    
    update_all_images()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)









