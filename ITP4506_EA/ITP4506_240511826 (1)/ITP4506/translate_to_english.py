#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to translate Chinese text to English in HTML files
This script will replace common Chinese phrases with their English equivalents
"""

import os
import re
from pathlib import Path

# Common translation mappings
TRANSLATIONS = {
    # Page titles
    r'<title>([^<]*?)</title>': lambda m: translate_title(m.group(1)),
    
    # HTML lang attribute
    r'lang="zh-CN"': 'lang="en"',
    
    # Common phrases (in order of specificity - more specific first)
    '二手交易平台': 'Smile &amp; Sunshine Toy Co. Ltd',
    '切换主题': 'Toggle Theme',
    '请登录': 'Please Login',
    '登录': 'Login',
    '注册': 'Register',
    '返回登录': 'Back to Login',
    '提交注册': 'Register',
    '忘记密码': 'Forgot Password',
    '记住我': 'Remember Me',
    '用户名': 'Username',
    '密码': 'Password',
    '邮箱': 'Email',
    '电话号码': 'Phone Number',
    '再次确认密码': 'Confirm Password',
    '二次验证码（可选）': 'Two-Factor Code (Optional)',
    '如未开启可留空': 'Leave empty if not enabled',
    '或': 'OR',
    '使用 Google 登录（占位）': 'Sign in with Google (Placeholder)',
    '请输入您的账户信息以继续': 'Please enter your account information to continue',
    '请填写以下信息创建账户': 'Please fill in the following information to create an account',
    '至少 6 位，包含大小写字母、数字和特殊字符中任意两种以上': 'At least 6 characters, containing at least two of: uppercase, lowercase, numbers, and special characters',
    '输入有误': 'Invalid input',
    '请输入用户名': 'Please enter username',
    '请输入密码': 'Please enter password',
    '请输入有效邮箱': 'Please enter a valid email',
    '请输入6-15位数字手机号': 'Please enter 6-15 digit phone number',
    '密码至少6位': 'Password must be at least 6 characters',
    '两次密码不一致': 'Passwords do not match',
    '请修正表单中的错误': 'Please correct the errors in the form',
    '正在登录...': 'Logging in...',
    '登录成功：': 'Login successful: ',
    '登录失败': 'Login failed',
    '注册失败': 'Registration failed',
    '注册成功，即将跳转到登录页...': 'Registration successful, redirecting to login page...',
    '请求失败：': 'Request failed: ',
    '正在打开 Google 登录...': 'Opening Google login...',
    'Google 登录失败': 'Google login failed',
    '请输入注册邮箱：': 'Please enter your registered email:',
    '已提交': 'Submitted',
    '响应不是JSON': 'Response is not JSON',
    '确定要退出登录吗？': 'Are you sure you want to logout?',
}

def translate_title(title):
    """Translate common title patterns"""
    title_translations = {
        '登录': 'Login',
        '注册': 'Register',
        '二手交易平台': 'Smile &amp; Sunshine Toy Co. Ltd',
        '交易对话': 'Messages',
        '在线客服': 'Online Support',
        '讨论区': 'Forum',
        '商品详情': 'Product Details',
        '官方商城': 'Official Store',
        '二手市场': 'Second-hand Market',
        '价格资讯': 'Price Info',
        '新闻中心': 'News Center',
        '我的物品': 'My Items',
        '我的收藏': 'My Favorites',
        '我的评价': 'My Reviews',
        '搜寻关键字通知': 'Search Notifications',
        '注视名单': 'Watchlist',
        '封锁名单': 'Blocklist',
        '手机认证': 'Phone Verification',
        '优惠券中心': 'Coupon Center',
        '申请退款': 'Refund Application',
        'AI推荐': 'AI Recommendations',
        '客户菜单': 'Customer Menu',
    }
    
    for chinese, english in title_translations.items():
        if chinese in title:
            title = title.replace(chinese, english)
    
    # Handle " - " separator
    if ' - ' in title:
        parts = title.split(' - ')
        if len(parts) == 2:
            return f"{parts[0]} - {parts[1]}"
    
    return title

def process_file(file_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply translations
        for chinese, english in TRANSLATIONS.items():
            if isinstance(english, str):
                content = content.replace(chinese, english)
            else:  # it's a regex function
                content = re.sub(chinese, english, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Processed: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    frontend_dir = Path('frontend')
    
    if not frontend_dir.exists():
        print("frontend directory not found!")
        return
    
    html_files = list(frontend_dir.rglob('*.html'))
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    processed = 0
    for html_file in html_files:
        if process_file(html_file):
            processed += 1
    
    print(f"\nProcessed {processed} files.")

if __name__ == '__main__':
    main()










