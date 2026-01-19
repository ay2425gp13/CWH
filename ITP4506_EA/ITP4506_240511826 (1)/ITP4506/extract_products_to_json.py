#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
提取 platform-market.html 中的商品数据到 JSON 文件
"""
import re
import json
import sys

def extract_products_data(html_file_path):
    """从 HTML 文件中提取 productsData 数组"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 productsData 数组的开始和结束位置
    start_pattern = r'const productsData = \['
    end_pattern = r'\];'
    
    start_match = re.search(start_pattern, content)
    if not start_match:
        print("错误：找不到 productsData 数组的开始位置")
        return None
    
    start_pos = start_match.end()
    
    # 从开始位置向后查找，找到匹配的 ];（考虑嵌套的数组和对象）
    bracket_count = 1
    pos = start_pos
    end_pos = None
    
    while pos < len(content):
        if content[pos] == '[':
            bracket_count += 1
        elif content[pos] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end_pos = pos + 1
                break
        pos += 1
    
    if end_pos is None:
        print("错误：找不到 productsData 数组的结束位置")
        return None
    
    # 提取数组内容
    array_content = content[start_pos:end_pos].strip()
    
    # 使用 eval 或 ast.literal_eval 来解析 JavaScript 对象
    # 但更安全的方法是手动解析或使用 JavaScript 引擎
    # 这里我们使用一个简化的方法：将 JavaScript 对象转换为 JSON
    
    # 替换 JavaScript 的 true/false/null 为 JSON 格式
    array_content = re.sub(r'\btrue\b', 'true', array_content)
    array_content = re.sub(r'\bfalse\b', 'false', array_content)
    array_content = re.sub(r'\bnull\b', 'null', array_content)
    
    # 尝试使用 exec 执行 JavaScript 代码（需要 Node.js 环境）
    # 或者手动解析
    
    # 更简单的方法：使用正则表达式提取每个商品对象
    products = []
    
    # 匹配商品对象：{ id: ..., title: ..., ... }
    # 使用更精确的正则表达式
    pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    
    # 更简单的方法：逐行解析
    lines = array_content.split('\n')
    current_product = {}
    in_product = False
    brace_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否是对象开始
        if line.startswith('{'):
            in_product = True
            brace_count = line.count('{') - line.count('}')
            current_product = {}
            # 解析第一行的属性
            if '}' not in line:
                # 继续解析属性
                pass
            else:
                # 单行对象
                pass
        
        # 解析属性
        if in_product:
            # 匹配 key: value 格式
            match = re.match(r'(\w+):\s*(.+?)(?:,|$)', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip().rstrip(',')
                
                # 移除引号
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # 尝试转换为数字
                elif value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                
                current_product[key] = value
            
            # 检查对象结束
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0 and '}' in line:
                products.append(current_product)
                current_product = {}
                in_product = False
                brace_count = 0
    
    # 如果上面的方法不行，使用更直接的方法：使用 JavaScript 引擎
    # 或者手动解析整个数组
    
    return products

def extract_products_simple(html_file_path):
    """使用更简单的方法：直接使用正则表达式提取所有商品对象"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 productsData 数组
    match = re.search(r'const productsData = \[(.*?)\];', content, re.DOTALL)
    if not match:
        print("错误：找不到 productsData 数组")
        return None
    
    array_content = match.group(1)
    
    # 使用正则表达式提取每个商品对象
    products = []
    
    # 匹配每个商品对象（考虑嵌套）
    product_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(product_pattern, array_content)
    
    for match in matches:
        obj_str = match.group(0)
        
        # 解析对象属性
        product = {}
        
        # 提取 id
        id_match = re.search(r'id:\s*(\d+)', obj_str)
        if id_match:
            product['id'] = int(id_match.group(1))
        
        # 提取 title
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', obj_str)
        if title_match:
            product['title'] = title_match.group(1)
        
        # 提取 price
        price_match = re.search(r'price:\s*(\d+(?:\.\d+)?)', obj_str)
        if price_match:
            product['price'] = float(price_match.group(1))
        
        # 提取 originalPrice
        original_price_match = re.search(r'originalPrice:\s*(\d+(?:\.\d+)?)', obj_str)
        if original_price_match:
            product['originalPrice'] = float(original_price_match.group(1))
        
        # 提取 image
        image_match = re.search(r'image:\s*["\']([^"\']+)["\']', obj_str)
        if image_match:
            product['image'] = image_match.group(1)
        
        # 提取 sales
        sales_match = re.search(r'sales:\s*(\d+)', obj_str)
        if sales_match:
            product['sales'] = int(sales_match.group(1))
        
        # 提取 location
        location_match = re.search(r'location:\s*["\']([^"\']+)["\']', obj_str)
        if location_match:
            product['location'] = location_match.group(1)
        
        # 提取 seller
        seller_match = re.search(r'seller:\s*["\']([^"\']+)["\']', obj_str)
        if seller_match:
            product['seller'] = seller_match.group(1)
        
        # 提取 shippingAddress
        shipping_match = re.search(r'shippingAddress:\s*["\']([^"\']+)["\']', obj_str)
        if shipping_match:
            product['shippingAddress'] = shipping_match.group(1)
        
        # 提取 badge
        badge_match = re.search(r'badge:\s*["\']([^"\']+)["\']', obj_str)
        if badge_match:
            product['badge'] = badge_match.group(1)
        
        # 提取 category
        category_match = re.search(r'category:\s*["\']([^"\']+)["\']', obj_str)
        if category_match:
            product['category'] = category_match.group(1)
        
        if product.get('id'):
            products.append(product)
    
    return products

if __name__ == '__main__':
    html_file = 'frontend/platform-market.html'
    output_file = 'frontend/data/products.json'
    
    print(f"正在从 {html_file} 提取商品数据...")
    products = extract_products_simple(html_file)
    
    if products:
        print(f"成功提取 {len(products)} 个商品")
        
        # 确保输出目录存在
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存到 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"商品数据已保存到 {output_file}")
        
        # 显示前几个商品作为示例
        print("\n前3个商品示例：")
        for i, product in enumerate(products[:3], 1):
            print(f"{i}. {product.get('title', 'N/A')} - {product.get('price', 'N/A')}元")
    else:
        print("提取失败，请检查 HTML 文件格式")
        sys.exit(1)




# -*- coding: utf-8 -*-
"""
提取 platform-market.html 中的商品数据到 JSON 文件
"""
import re
import json
import sys

def extract_products_data(html_file_path):
    """从 HTML 文件中提取 productsData 数组"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 productsData 数组的开始和结束位置
    start_pattern = r'const productsData = \['
    end_pattern = r'\];'
    
    start_match = re.search(start_pattern, content)
    if not start_match:
        print("错误：找不到 productsData 数组的开始位置")
        return None
    
    start_pos = start_match.end()
    
    # 从开始位置向后查找，找到匹配的 ];（考虑嵌套的数组和对象）
    bracket_count = 1
    pos = start_pos
    end_pos = None
    
    while pos < len(content):
        if content[pos] == '[':
            bracket_count += 1
        elif content[pos] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end_pos = pos + 1
                break
        pos += 1
    
    if end_pos is None:
        print("错误：找不到 productsData 数组的结束位置")
        return None
    
    # 提取数组内容
    array_content = content[start_pos:end_pos].strip()
    
    # 使用 eval 或 ast.literal_eval 来解析 JavaScript 对象
    # 但更安全的方法是手动解析或使用 JavaScript 引擎
    # 这里我们使用一个简化的方法：将 JavaScript 对象转换为 JSON
    
    # 替换 JavaScript 的 true/false/null 为 JSON 格式
    array_content = re.sub(r'\btrue\b', 'true', array_content)
    array_content = re.sub(r'\bfalse\b', 'false', array_content)
    array_content = re.sub(r'\bnull\b', 'null', array_content)
    
    # 尝试使用 exec 执行 JavaScript 代码（需要 Node.js 环境）
    # 或者手动解析
    
    # 更简单的方法：使用正则表达式提取每个商品对象
    products = []
    
    # 匹配商品对象：{ id: ..., title: ..., ... }
    # 使用更精确的正则表达式
    pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    
    # 更简单的方法：逐行解析
    lines = array_content.split('\n')
    current_product = {}
    in_product = False
    brace_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否是对象开始
        if line.startswith('{'):
            in_product = True
            brace_count = line.count('{') - line.count('}')
            current_product = {}
            # 解析第一行的属性
            if '}' not in line:
                # 继续解析属性
                pass
            else:
                # 单行对象
                pass
        
        # 解析属性
        if in_product:
            # 匹配 key: value 格式
            match = re.match(r'(\w+):\s*(.+?)(?:,|$)', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip().rstrip(',')
                
                # 移除引号
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # 尝试转换为数字
                elif value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                
                current_product[key] = value
            
            # 检查对象结束
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0 and '}' in line:
                products.append(current_product)
                current_product = {}
                in_product = False
                brace_count = 0
    
    # 如果上面的方法不行，使用更直接的方法：使用 JavaScript 引擎
    # 或者手动解析整个数组
    
    return products

def extract_products_simple(html_file_path):
    """使用更简单的方法：直接使用正则表达式提取所有商品对象"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 productsData 数组
    match = re.search(r'const productsData = \[(.*?)\];', content, re.DOTALL)
    if not match:
        print("错误：找不到 productsData 数组")
        return None
    
    array_content = match.group(1)
    
    # 使用正则表达式提取每个商品对象
    products = []
    
    # 匹配每个商品对象（考虑嵌套）
    product_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(product_pattern, array_content)
    
    for match in matches:
        obj_str = match.group(0)
        
        # 解析对象属性
        product = {}
        
        # 提取 id
        id_match = re.search(r'id:\s*(\d+)', obj_str)
        if id_match:
            product['id'] = int(id_match.group(1))
        
        # 提取 title
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', obj_str)
        if title_match:
            product['title'] = title_match.group(1)
        
        # 提取 price
        price_match = re.search(r'price:\s*(\d+(?:\.\d+)?)', obj_str)
        if price_match:
            product['price'] = float(price_match.group(1))
        
        # 提取 originalPrice
        original_price_match = re.search(r'originalPrice:\s*(\d+(?:\.\d+)?)', obj_str)
        if original_price_match:
            product['originalPrice'] = float(original_price_match.group(1))
        
        # 提取 image
        image_match = re.search(r'image:\s*["\']([^"\']+)["\']', obj_str)
        if image_match:
            product['image'] = image_match.group(1)
        
        # 提取 sales
        sales_match = re.search(r'sales:\s*(\d+)', obj_str)
        if sales_match:
            product['sales'] = int(sales_match.group(1))
        
        # 提取 location
        location_match = re.search(r'location:\s*["\']([^"\']+)["\']', obj_str)
        if location_match:
            product['location'] = location_match.group(1)
        
        # 提取 seller
        seller_match = re.search(r'seller:\s*["\']([^"\']+)["\']', obj_str)
        if seller_match:
            product['seller'] = seller_match.group(1)
        
        # 提取 shippingAddress
        shipping_match = re.search(r'shippingAddress:\s*["\']([^"\']+)["\']', obj_str)
        if shipping_match:
            product['shippingAddress'] = shipping_match.group(1)
        
        # 提取 badge
        badge_match = re.search(r'badge:\s*["\']([^"\']+)["\']', obj_str)
        if badge_match:
            product['badge'] = badge_match.group(1)
        
        # 提取 category
        category_match = re.search(r'category:\s*["\']([^"\']+)["\']', obj_str)
        if category_match:
            product['category'] = category_match.group(1)
        
        if product.get('id'):
            products.append(product)
    
    return products

if __name__ == '__main__':
    html_file = 'frontend/platform-market.html'
    output_file = 'frontend/data/products.json'
    
    print(f"正在从 {html_file} 提取商品数据...")
    products = extract_products_simple(html_file)
    
    if products:
        print(f"成功提取 {len(products)} 个商品")
        
        # 确保输出目录存在
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存到 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"商品数据已保存到 {output_file}")
        
        # 显示前几个商品作为示例
        print("\n前3个商品示例：")
        for i, product in enumerate(products[:3], 1):
            print(f"{i}. {product.get('title', 'N/A')} - {product.get('price', 'N/A')}元")
    else:
        print("提取失败，请检查 HTML 文件格式")
        sys.exit(1)








