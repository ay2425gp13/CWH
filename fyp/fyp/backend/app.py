from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config as config_dict
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime
from models import db, User, Product, Category, Order, Review, Favorite, Watchlist, Notification
import openai

def create_app(config_name=None):
    app = Flask(__name__)
    # Enable CORS for local development and file:// origin
    CORS(
        app,
        resources={r"/*": {"origins": ["*", "null", "http://localhost:*", "http://127.0.0.1:*"]}},
        supports_credentials=False,
    )
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config_dict[config_name])
    
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化数据库
    db.init_app(app)
    
    # Note: 之前的内存 users 已不再用于认证，以下新增基于数据库的认证接口

    # Frontend directory (login page and assets)
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    
    @app.route('/')
    def index():
        return redirect(url_for('serve_login_page'))

    @app.route('/api')
    def api_status():
        return jsonify({"message": "Second-hand Marketplace API", "status": "running"})

    # Serve frontend login page and assets so others can open via http://<IP>:5000/login
    @app.route('/login')
    def serve_login_page():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/css/<path:filename>')
    def serve_css(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'assets'), filename)

    @app.route('/my-items')
    def my_items_page():
        return send_from_directory(frontend_dir, 'my-items.html')

    # 兼容直接访问 .html 结尾
    @app.route('/my-items.html')
    def my_items_page_html():
        return send_from_directory(frontend_dir, 'my-items.html')

    @app.route('/my-reviews')
    def my_reviews_page():
        return send_from_directory(frontend_dir, 'my-reviews.html')

    @app.route('/my-reviews.html')
    def my_reviews_page_html():
        return send_from_directory(frontend_dir, 'my-reviews.html')

    @app.route('/search-notifications')
    def search_notifications_page():
        return send_from_directory(frontend_dir, 'search-notifications.html')

    @app.route('/search-notifications.html')
    def search_notifications_page_html():
        return send_from_directory(frontend_dir, 'search-notifications.html')

    @app.route('/my-favorites')
    def my_favorites_page():
        return send_from_directory(frontend_dir, 'my-favorites.html')

    @app.route('/my-favorites.html')
    def my_favorites_page_html():
        return send_from_directory(frontend_dir, 'my-favorites.html')

    @app.route('/menu')
    def serve_customer_menu():
        return send_from_directory(frontend_dir, 'CustomerMenu.html')

    @app.route('/CustomerMenu.html')
    def serve_customer_menu_direct():
        return send_from_directory(frontend_dir, 'CustomerMenu.html')

    @app.route('/news.html')
    def serve_news_direct():
        return send_from_directory(frontend_dir, 'news.html')

    @app.route('/prices.html')
    def serve_prices_direct():
        return send_from_directory(frontend_dir, 'prices.html')

    @app.route('/forum.html')
    def serve_forum_direct():
        return send_from_directory(frontend_dir, 'forum.html')

    @app.route('/secondary.html')
    def serve_secondary_direct():
        return send_from_directory(frontend_dir, 'secondary.html')

    @app.route('/platform-market.html')
    def serve_platform_market():
        return send_from_directory(frontend_dir, 'platform-market.html')

    @app.route('/online-support.html')
    def serve_online_support():
        return send_from_directory(frontend_dir, 'online-support.html')

    @app.route('/product-detail.html')
    def serve_product_detail():
        return send_from_directory(frontend_dir, 'product-detail.html')

    @app.route('/AI-Setup-Recommend.html')
    def serve_ai_setup_recommend():
        return send_from_directory(frontend_dir, 'AI-Setup-Recommend.html')

    @app.route('/friendlist.html')
    def serve_friendlist():
        return send_from_directory(frontend_dir, 'friendlist.html')

    @app.route('/gift-box.html')
    def serve_gift_box():
        return send_from_directory(frontend_dir, 'gift-box.html')

    @app.route('/coupon.html')
    def serve_coupon():
        return send_from_directory(frontend_dir, 'coupon.html')

    @app.route('/refund.html')
    def serve_refund():
        return send_from_directory(frontend_dir, 'refund.html')

    @app.route('/forum.html')
    def serve_forum():
        return send_from_directory(frontend_dir, 'forum.html')

    @app.route('/nav-test.html')
    def serve_nav_test():
        return send_from_directory(frontend_dir, 'nav-test.html')

    @app.route('/api/user/info')
    def get_user_info():
        # 从session中获取用户信息
        user_info = session.get('user_info', {
            'id': '7758',
            'username': '中俊',
            'avatar': '',
            'registration_time': '2024-01-15',
            'is_new_user': True,
            'phone_verified': False,
            'email_verified': False
        })
        return jsonify(user_info)

    @app.route('/api/user/items')
    def get_user_items():
        # 模拟用户物品数据
        user_items = [
            {
                'id': 1,
                'title': 'iPhone 13 128GB 蓝色 99新',
                'price': 2680,
                'status': '进行中',
                'image': 'https://via.placeholder.com/300x200/007AFF/FFFFFF?text=iPhone+13',
                'views': 156,
                'favorites': 23,
                'date': '2024-01-15',
                'category': '手机'
            },
            {
                'id': 2,
                'title': 'Sony A6400 微单相机 套机',
                'price': 3500,
                'status': '已售出',
                'image': 'https://via.placeholder.com/300x200/FF6B35/FFFFFF?text=A6400',
                'views': 89,
                'favorites': 12,
                'date': '2024-01-10',
                'category': '摄影'
            }
        ]
        return jsonify(user_items)

    @app.route('/api/user/reviews/received')
    def get_received_reviews():
        # 模拟收到的评价数据
        received_reviews = [
            {
                'id': 1,
                'reviewer_name': '张先生',
                'reviewer_id': '1234',
                'rating': 5,
                'comment': '交易很顺利，物品质量很好，推荐！',
                'date': '2024-01-10',
                'item_title': 'iPhone 13 128GB',
                'item_id': 1,
                'can_respond': True,
                'response': None
            },
            {
                'id': 2,
                'reviewer_name': '李女士',
                'reviewer_id': '5678',
                'rating': 4,
                'comment': '卖家很负责任，包装很好。',
                'date': '2024-01-08',
                'item_title': 'Sony A6400 相机',
                'item_id': 2,
                'can_respond': False,
                'response': '谢谢您的评价！'
            }
        ]
        return jsonify(received_reviews)

    @app.route('/api/user/reviews/given')
    def get_given_reviews():
        # 模拟给出的评价数据
        given_reviews = [
            {
                'id': 1,
                'seller_name': '王先生',
                'seller_id': '9999',
                'rating': 5,
                'comment': '卖家很专业，物品描述准确，推荐！',
                'date': '2024-01-12',
                'item_title': 'Canon 24-70mm 镜头',
                'item_id': 3
            },
            {
                'id': 2,
                'seller_name': '陈女士',
                'seller_id': '8888',
                'rating': 4,
                'comment': '交易顺利，物品质量不错。',
                'date': '2024-01-05',
                'item_title': 'AirPods Pro',
                'item_id': 4
            }
        ]
        return jsonify(given_reviews)

    @app.route('/api/user/reviews/respond', methods=['POST'])
    def respond_to_review():
        data = request.get_json()
        review_id = data.get('review_id')
        response_text = data.get('response')
        
        # 模拟回应评价
        return jsonify({
            'success': True,
            'message': '回应已提交'
        })


    @app.route('/api/user/notifications/settings', methods=['POST'])
    def update_notification_settings():
        data = request.get_json()
        
        # 模拟更新通知设置
        return jsonify({
            'success': True,
            'message': '设置已保存'
        })

    @app.route('/api/user/notifications/keywords', methods=['POST'])
    def add_keyword():
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': '关键字不能为空'
            }), 400
        
        # 模拟添加关键字
        return jsonify({
            'success': True,
            'message': '关键字已添加'
        })

    @app.route('/api/user/notifications/keywords/<keyword>', methods=['DELETE'])
    def delete_keyword(keyword):
        # 模拟删除关键字
        return jsonify({
            'success': True,
            'message': '关键字已删除'
        })

    @app.route('/api/user/notifications/settings')
    def get_notification_settings():
        # 模拟通知设置数据
        settings = {
            'email_notifications': True,
            'push_notifications': True,
            'keywords': [
                {
                    'id': 1,
                    'keyword': 'iPhone',
                    'created_at': '2024-01-10',
                    'active': True
                },
                {
                    'id': 2,
                    'keyword': 'Sony相机',
                    'created_at': '2024-01-08',
                    'active': True
                }
            ]
        }
        return jsonify(settings)




    @app.route('/api/user/notifications/keywords/<int:keyword_id>/toggle', methods=['POST'])
    def toggle_keyword(keyword_id):
        data = request.get_json()
        active = data.get('active', True)
        
        # 模拟切换关键字状态
        return jsonify({
            'success': True,
            'message': '关键字状态已更新',
            'active': active
        })

    # 全局收藏存储（实际应用中应该使用数据库）
    user_favorites = {}
    
    @app.route('/api/user/favorites')
    def get_user_favorites():
        # 获取当前用户ID
        user_info = session.get('user_info', {})
        user_id = user_info.get('id', 'default')
        
        # 返回用户的收藏列表
        favorites = user_favorites.get(user_id, [])
        return jsonify(favorites)

    @app.route('/api/user/favorites', methods=['POST'])
    def add_to_favorites():
        data = request.get_json()
        item_id = data.get('item_id')
        
        if not item_id:
            return jsonify({
                'success': False,
                'message': '商品ID不能为空'
            }), 400
        
        # 获取当前用户ID
        user_info = session.get('user_info', {})
        user_id = user_info.get('id', 'default')
        
        # 初始化用户收藏列表
        if user_id not in user_favorites:
            user_favorites[user_id] = []
        
        # 检查是否已经收藏
        existing_favorite = next((f for f in user_favorites[user_id] if f['item_id'] == item_id), None)
        if existing_favorite:
            return jsonify({
                'success': False,
                'message': '该商品已在收藏列表中'
            })
        
        # 添加到收藏
        favorite_item = {
            'id': len(user_favorites[user_id]) + 1,
            'item_id': item_id,
            'title': data.get('title', f'商品 {item_id}'),
            'price': data.get('price', 0),
            'image': data.get('image', 'https://via.placeholder.com/300x200?text=Product'),
            'seller': data.get('seller', '卖家'),
            'location': data.get('location', '香港'),
            'category': data.get('category', '其他'),
            'favorited_at': datetime.now().strftime('%Y-%m-%d'),
            'status': '进行中'
        }
        
        user_favorites[user_id].append(favorite_item)
        
        return jsonify({
            'success': True,
            'message': '已添加到收藏'
        })

    @app.route('/api/user/favorites/<int:favorite_id>', methods=['DELETE'])
    def remove_from_favorites(favorite_id):
        # 获取当前用户ID
        user_info = session.get('user_info', {})
        user_id = user_info.get('id', 'default')
        
        if user_id not in user_favorites:
            return jsonify({
                'success': False,
                'message': '收藏列表为空'
            })
        
        # 查找并移除收藏
        user_favorites[user_id] = [f for f in user_favorites[user_id] if f['id'] != favorite_id]
        
        return jsonify({
            'success': True,
            'message': '已从收藏中移除'
        })

    @app.route('/api/user/favorites/clear', methods=['POST'])
    def clear_all_favorites():
        # 获取当前用户ID
        user_info = session.get('user_info', {})
        user_id = user_info.get('id', 'default')
        
        # 清空用户收藏
        user_favorites[user_id] = []
        
        return jsonify({
            'success': True,
            'message': '已清空所有收藏'
        })

    # 商品相关API
    @app.route('/api/products')
    def get_products():
        """获取商品列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category', '')
        search = request.args.get('search', '')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 新增筛选参数
        condition = request.args.get('condition', '')  # 成色筛选
        min_price = request.args.get('min_price', type=float)  # 最低价格
        max_price = request.args.get('max_price', type=float)  # 最高价格
        location = request.args.get('location', '')  # 区域筛选
        
        query = Product.query.filter(Product.status == 'active')
        
        # 分类筛选
        if category and category != '全部':
            query = query.filter(Product.category.has(name=category))
        
        # 搜索筛选
        if search:
            query = query.filter(
                db.or_(
                    Product.name.contains(search),
                    Product.description.contains(search),
                    Product.brand.contains(search)
                )
            )
        
        # 成色筛选
        if condition:
            query = query.filter(Product.condition == condition)
        
        # 价格范围筛选
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # 区域筛选
        if location:
            query = query.filter(Product.location.contains(location))
        
        # 排序
        if sort_by == 'price':
            if sort_order == 'asc':
                query = query.order_by(Product.price.asc())
            else:
                query = query.order_by(Product.price.desc())
        elif sort_by == 'views':
            query = query.order_by(Product.views.desc())
        elif sort_by == 'favorites':
            query = query.order_by(Product.favorites.desc())
        else:
            query = query.order_by(Product.created_at.desc())
        
        # 分页
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': [{
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': p.price,
                'original_price': p.original_price,
                'condition': p.condition,
                'brand': p.brand,
                'location': p.location,
                'images': p.images,
                'tags': p.tags,
                'stock': p.stock,
                'views': p.views,
                'favorites': p.favorites,
                'is_new': p.is_new,
                'created_at': p.created_at.isoformat(),
                'seller': {
                    'id': p.seller.id,
                    'username': p.seller.username,
                    'rating': p.seller.rating,
                    'sales_count': p.seller.sales_count
                }
            } for p in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        })

    @app.route('/api/products/<int:product_id>')
    def get_product_detail(product_id):
        """获取单个商品详情"""
        product = Product.query.get_or_404(product_id)
        
        # 增加浏览次数
        product.views += 1
        db.session.commit()
        
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'original_price': product.original_price,
            'condition': product.condition,
            'brand': product.brand,
            'location': product.location,
            'images': product.images,
            'tags': product.tags,
            'stock': product.stock,
            'views': product.views,
            'favorites': product.favorites,
            'is_new': product.is_new,
            'created_at': product.created_at.isoformat(),
            'category': {
                'id': product.category.id,
                'name': product.category.name
            },
            'seller': {
                'id': product.seller.id,
                'username': product.seller.username,
                'rating': product.seller.rating,
                'sales_count': product.seller.sales_count
            }
        })

    @app.route('/api/products/<int:product_id>/favorite', methods=['POST'])
    def toggle_favorite(product_id):
        """切换收藏状态"""
        user_info = session.get('user_info', {})
        user_id = user_info.get('id')
        
        if not user_id:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        product = Product.query.get_or_404(product_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': '用户不存在'}), 404
        
        # 检查是否已收藏
        favorite = Favorite.query.filter_by(
            user_id=user_id, product_id=product_id
        ).first()
        
        if favorite:
            # 取消收藏
            db.session.delete(favorite)
            product.favorites -= 1
            message = '已取消收藏'
        else:
            # 添加收藏
            favorite = Favorite(user_id=user_id, product_id=product_id)
            db.session.add(favorite)
            product.favorites += 1
            message = '已添加到收藏'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': message,
            'favorites_count': product.favorites
        })

    @app.route('/api/products/<int:product_id>/watch', methods=['POST'])
    def toggle_watch(product_id):
        """切换关注卖家状态"""
        user_info = session.get('user_info', {})
        user_id = user_info.get('id')
        
        if not user_id:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        product = Product.query.get_or_404(product_id)
        seller_id = product.seller_id
        
        if user_id == seller_id:
            return jsonify({'success': False, 'message': '不能关注自己'}), 400
        
        # 检查是否已关注
        watch = Watchlist.query.filter_by(
            user_id=user_id, seller_id=seller_id
        ).first()
        
        if watch:
            # 取消关注
            db.session.delete(watch)
            message = '已取消关注'
        else:
            # 添加关注
            watch = Watchlist(user_id=user_id, seller_id=seller_id)
            db.session.add(watch)
            message = '已关注卖家'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': message
        })

    @app.route('/signup')
    def serve_register_page():
        return send_from_directory(frontend_dir, 'register.html')

    # Additional frontend pages
    @app.route('/secondary')
    def serve_secondary_page():
        return send_from_directory(frontend_dir, 'secondary.html')

    @app.route('/news')
    def serve_news_page():
        return send_from_directory(frontend_dir, 'news.html')

    @app.route('/prices')
    def serve_prices_page():
        return send_from_directory(frontend_dir, 'prices.html')

    @app.route('/forum')
    def serve_forum_page():
        return send_from_directory(frontend_dir, 'forum.html')
    
    # ------------------ 基于数据库的认证接口 ------------------
    @app.route('/api/auth/register', methods=['POST'])
    def api_auth_register():
        data = request.get_json() or {}
        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip()
        password = data.get('password') or ''

        if not username or not email or not password:
            return jsonify({"success": False, "message": "用户名、邮箱和密码不能为空"}), 400

        # 唯一性检查
        existing_user = User.query.filter(
            db.or_(User.username == username, User.email == email)
        ).first()
        if existing_user:
            return jsonify({"success": False, "message": "用户名或邮箱已存在"}), 400

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "注册成功",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201

    @app.route('/api/auth/login', methods=['POST'])
    def api_auth_login():
        data = request.get_json() or {}
        account = (data.get('account') or data.get('username') or data.get('email') or '').strip()
        password = data.get('password') or ''
        remember = bool(data.get('remember', False))

        if not account or not password:
            return jsonify({"success": False, "message": "账号和密码不能为空"}), 400

        user = User.query.filter(
            db.or_(User.username == account, User.email == account)
        ).first()

        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"success": False, "message": "账号或密码错误"}), 401

        # 设置会话
        session['user'] = user.username
        session['logged_in'] = True
        session['user_info'] = {
            'id': str(user.id),
            'username': user.username,
            'avatar': user.avatar or '',
            'registration_time': user.created_at.strftime('%Y-%m-%d'),
            'is_new_user': False,
            'phone_verified': False,
            'email_verified': True if user.email else False
        }

        if remember:
            session.permanent = True

        return jsonify({
            "success": True,
            "message": "登录成功",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

    @app.route('/api/auth/logout', methods=['POST'])
    def api_auth_logout():
        session.pop('user', None)
        session.pop('logged_in', None)
        session.pop('user_info', None)
        return jsonify({"success": True, "message": "已退出登录"})

    @app.route('/api/pc-builder', methods=['POST'])
    def pc_builder():
        print("=== PC Builder API called ===")
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        print(f"Received message: {user_message}")
        
        if not user_message:
            print("No message provided")
            return jsonify({"success": False, "message": "Message is required"}), 400
        
        try:
            # Set OpenAI API key (you need to set OPENAI_API_KEY in environment or config)
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                # Mock response for testing
                message_lower = user_message.lower()
                
                # Check if this is a PC build request (contains build/pc) or specific component request
                is_pc_build = 'build' in message_lower or 'pc' in message_lower or 'computer' in message_lower
                is_cpu_request = 'cpu' in message_lower and not is_pc_build
                is_gpu_request = 'gpu' in message_lower and not is_pc_build  
                is_ram_request = 'ram' in message_lower and not is_pc_build
                
                if is_cpu_request:
                    print("DEBUG: Returning CPU response")
                    mock_responses = [
                        'The "best" CPU for gaming depends on your specific needs, such as your budget, resolution you\'re aiming for (1080p, 1440p, 4K), and whether you plan to stream, multitask, or use the system for other tasks like content creation. Here\'s a breakdown of the top CPUs in different categories:\n\n### **1. Best Overall Gaming CPU (2026)**  \n**Intel Core i9-14600K / i9-14600KF**  \n   - **Cores/Threads**: 14 cores (6 P-cores + 8 E-cores) / 20 threads\n   - **Base/Boost Clock**: 3.5 GHz base, up to 5.3 GHz boost\n   - **Socket**: LGA 1700\n   - **Why?**:  \n     - Excellent for 1440p and 4K gaming with the ability to handle multitasking and streaming.\n     - The 14-core design (6 high-performance cores + 8 efficiency cores) provides amazing performance in demanding games while multitasking or running background apps.\n     - Best for high-FPS gaming, multitasking, and content creation due to the massive core count.\n   - **Best for**: Enthusiasts who want the highest performance for 1440p/4K gaming and multitasking.\n\n---\n\n### **2. Best Mid-Range Gaming CPU**  \n**AMD Ryzen 5 7600X**  \n   - **Cores/Threads**: 6/12\n   - **Base/Boost Clock**: 4.7 GHz / 5.3 GHz\n   - **Socket**: AM5\n   - **Why?**:  \n     - Outstanding single-threaded and multi-threaded performance for gaming, perfect for 1080p and 1440p gaming.\n     - PCIe 5.0 and DDR5 support for future-proofing.\n     - Excellent performance in current-gen games, offering a balance of price and power.\n   - **Best for**: Gamers looking for great 1080p/1440p performance without breaking the bank.\n\n---\n\n### **3. Best Budget Gaming CPU**  \n**Intel Core i5-12400F**  \n   - **Cores/Threads**: 6/12\n   - **Base/Boost Clock**: 2.5 GHz / 4.4 GHz\n   - **Socket**: LGA 1700\n   - **Why?**:  \n     - Offers great performance for **1080p gaming** without the high price tag.\n     - Excellent single-core performance, which is key for many games.\n     - Low power consumption (65W TDP), making it an efficient option.\n     - No integrated graphics (F-series), so it\'s ideal if you have a dedicated GPU.\n   - **Best for**: Gamers on a budget who still want great gaming performance at 1080p.\n\n---\n\n### **4. Best for 4K Gaming & Streaming**  \n**AMD Ryzen 9 7900X3D**  \n   - **Cores/Threads**: 12/24\n   - **Base/Boost Clock**: 4.4 GHz / 5.6 GHz (3D V-cache)\n   - **Socket**: AM5\n   - **Why?**:  \n     - One of the best for **4K gaming** and heavy multitasking.\n     - **3D V-Cache** enhances gaming performance, especially in CPU-intensive titles (e.g., *Shadow of the Tomb Raider*).\n     - Fantastic at **streaming** while gaming, handling multiple threads efficiently.\n   - **Best for**: High-end 4K gaming, streaming, and content creation.\n\n---\n\n### **5. Best for Competitive Gaming (Esports)**  \n**Intel Core i3-12100F**  \n   - **Cores/Threads**: 4/8\n   - **Base/Boost Clock**: 3.3 GHz / 4.3 GHz\n   - **Socket**: LGA 1700\n   - **Why?**:  \n     - **Incredible single-core performance**, which is crucial for esports titles like *CS:GO*, *Valorant*, and *Apex Legends*.\n     - High FPS in **1080p** gaming with a lower price point.\n     - Supports **DDR4/DDR5** RAM, offering flexibility in budget builds.\n   - **Best for**: Competitive gamers who want the most FPS for titles that depend on high single-core performance.\n\n---\n\n### **Summary**:\n- **Best overall**: **Intel Core i9-14600K** for top-tier performance in gaming and multitasking.\n- **Best mid-range**: **AMD Ryzen 5 7600X** for great all-around gaming performance at a reasonable price.\n- **Best budget**: **Intel Core i5-12400F** for efficient 1080p gaming.\n- **Best for 4K/Streaming**: **AMD Ryzen 9 7900X3D** with advanced 3D V-cache for high-end gaming and multitasking.\n- **Best for competitive gaming**: **Intel Core i3-12100F** for high FPS in esports games.\n\nIf you\'re targeting a specific type of gaming or want more details on any of these, let me know!'
                    ]
                elif is_gpu_request:
                    mock_responses = [
                        'Choosing the best GPU for gaming depends on your budget, resolution, and desired frame rates. Here\'s a breakdown of the top GPUs in different categories for 2026:\n\n### **1. Best Overall Gaming GPU (2026)**  \n**NVIDIA GeForce RTX 4090**  \n   - **VRAM**: 24GB GDDR6X\n   - **Architecture**: Ada Lovelace\n   - **Why?**:  \n     - Unmatched performance for **4K gaming** with ray tracing and DLSS 3.\n     - Excellent for content creation, 3D rendering, and AI workloads.\n     - Future-proof with support for the latest technologies.\n   - **Best for**: Enthusiasts who want the absolute best performance for 4K gaming and beyond.\n\n---\n\n### **2. Best Mid-Range Gaming GPU**  \n**NVIDIA GeForce RTX 4070 Ti**  \n   - **VRAM**: 12GB GDDR6X\n   - **Architecture**: Ada Lovelace\n   - **Why?**:  \n     - Outstanding performance for **1440p and 4K gaming** at high settings.\n     - Excellent ray tracing capabilities and DLSS 3 support.\n     - Great value for the performance it offers.\n   - **Best for**: Gamers looking for high-end performance without the premium price.\n\n---\n\n### **3. Best Budget Gaming GPU**  \n**NVIDIA GeForce RTX 4060**  \n   - **VRAM**: 8GB GDDR6\n   - **Architecture**: Ada Lovelace\n   - **Why?**:  \n     - Excellent for **1080p and 1440p gaming** at high settings.\n     - Supports ray tracing and DLSS 3 for future-proofing.\n     - Great performance per dollar, making it ideal for budget builds.\n   - **Best for**: Gamers on a budget who still want modern features and good performance.\n\n---\n\n### **4. Best for 4K Gaming**  \n**NVIDIA GeForce RTX 4080**  \n   - **VRAM**: 16GB GDDR6X\n   - **Architecture**: Ada Lovelace\n   - **Why?**:  \n     - Perfect for **4K gaming** with high frame rates and ray tracing.\n     - Excellent for content creation and multitasking.\n     - Balances performance and price well for 4K enthusiasts.\n   - **Best for**: Gamers focused on 4K resolution with smooth frame rates.\n\n---\n\n### **5. Best for Competitive Gaming (Esports)**  \n**NVIDIA GeForce RTX 4060 Ti**  \n   - **VRAM**: 8GB GDDR6\n   - **Architecture**: Ada Lovelace\n   - **Why?**:  \n     - High frame rates for **1080p gaming** in competitive titles.\n     - Excellent ray tracing and DLSS support for modern games.\n     - Efficient power consumption and good value.\n   - **Best for**: Esports gamers who need high FPS in fast-paced games.\n\n---\n\n### **AMD Alternatives**:\n- **AMD Radeon RX 7900 XTX**: Best overall AMD GPU, great for 4K gaming and content creation.\n- **AMD Radeon RX 7800 XT**: Mid-range option with excellent performance for 1440p gaming.\n- **AMD Radeon RX 7600**: Budget-friendly option for 1080p gaming.\n\n### **Summary**:\n- **Best overall**: **RTX 4090** for ultimate performance.\n- **Best mid-range**: **RTX 4070 Ti** for excellent 1440p/4K gaming.\n- **Best budget**: **RTX 4060** for great 1080p/1440p performance.\n- **Best for 4K**: **RTX 4080** for smooth 4K gaming.\n- **Best for competitive gaming**: **RTX 4060 Ti** for high FPS.\n\nConsider your monitor resolution, refresh rate, and budget when choosing. If you\'re targeting a specific resolution or have a budget in mind, let me know for more tailored recommendations!'
                    ]
                elif is_ram_request:
                    mock_responses = [
                        'RAM (Random Access Memory) is crucial for gaming performance, multitasking, and overall system responsiveness. Here\'s a comprehensive guide to choosing the best RAM for gaming in 2026:\n\n### **1. Best Overall Gaming RAM (2026)**  \n**Corsair Vengeance RGB DDR5-6000 (32GB)**  \n   - **Capacity**: 32GB (2x16GB)\n   - **Speed**: 6000MHz\n   - **Latency**: CL30\n   - **Voltage**: 1.35V\n   - **Why?**:  \n     - Excellent performance for gaming and content creation.\n     - High-speed DDR5 with low latency for maximum gaming performance.\n     - RGB lighting for aesthetics and future-proofing.\n   - **Best for**: Enthusiasts who want the best performance and are willing to pay a premium.\n\n---\n\n### **2. Best Mid-Range Gaming RAM**  \n**G.Skill Ripjaws V DDR5-5600 (16GB)**  \n   - **Capacity**: 16GB (2x8GB)\n   - **Speed**: 5600MHz\n   - **Latency**: CL36\n   - **Voltage**: 1.25V\n   - **Why?**:  \n     - Great balance of performance and price for 1080p/1440p gaming.\n     - Reliable DDR5 memory with good overclocking potential.\n     - Compatible with most modern motherboards.\n   - **Best for**: Gamers looking for solid performance without breaking the bank.\n\n---\n\n### **3. Best Budget Gaming RAM**  \n**Corsair Vengeance LPX DDR4-3200 (16GB)**  \n   - **Capacity**: 16GB (2x8GB)\n   - **Speed**: 3200MHz\n   - **Latency**: CL16\n   - **Voltage**: 1.35V\n   - **Why?**:  \n     - Excellent value for budget gaming builds.\n     - Low-profile design for better cooler compatibility.\n     - Proven reliability and performance for 1080p gaming.\n   - **Best for**: Budget-conscious gamers who still want quality components.\n\n---\n\n### **4. Best for High-End Gaming & Content Creation**  \n**Kingston Fury Beast DDR5-6000 (32GB)**  \n   - **Capacity**: 32GB (2x16GB)\n   - **Speed**: 6000MHz\n   - **Latency**: CL30\n   - **Voltage**: 1.35V\n   - **Why?**:  \n     - Perfect for 4K gaming, streaming, and video editing.\n     - High capacity and speed for demanding workloads.\n     - Excellent thermal performance and stability.\n   - **Best for**: Content creators and high-end gamers who need maximum performance.\n\n---\n\n### **5. Best for Competitive Gaming (Esports)**  \n**TeamGroup T-Force XTREEM DDR4-3600 (16GB)**  \n   - **Capacity**: 16GB (2x8GB)\n   - **Speed**: 3600MHz\n   - **Latency**: CL14\n   - **Voltage**: 1.35V\n   - **Why?**:  \n     - Low latency for maximum frame rates in competitive games.\n     - High-speed DDR4 for esports titles.\n     - Reliable performance with minimal input lag.\n   - **Best for**: Competitive gamers who need every advantage in fast-paced games.\n\n---\n\n### **Key Considerations for Gaming RAM**:\n\n#### **Capacity**:\n- **Minimum**: 16GB for modern gaming\n- **Recommended**: 16GB for gaming, 32GB for content creation/streaming\n- **Future-proof**: 32GB+ for longevity\n\n#### **Speed**:\n- **DDR4**: 3200MHz minimum, 3600MHz+ recommended\n- **DDR5**: 5200MHz minimum, 5600MHz+ recommended\n\n#### **Latency**:\n- Lower CL numbers (e.g., CL14 vs CL16) = better performance\n- Balance speed and latency for optimal gaming performance\n\n#### **Dual-Channel**:\n- Always use 2 sticks (matched pair) for dual-channel memory\n- Avoid single sticks for gaming builds\n\n### **DDR4 vs DDR5**:\n- **DDR4**: More affordable, widely compatible, excellent for budget/mid-range builds\n- **DDR5**: Future-proof, higher speeds, better for high-end builds\n\n### **Summary**:\n- **Best overall**: **Corsair Vengeance RGB DDR5-6000 (32GB)** for ultimate performance.\n- **Best mid-range**: **G.Skill Ripjaws V DDR5-5600 (16GB)** for great value.\n- **Best budget**: **Corsair Vengeance LPX DDR4-3200 (16GB)** for affordability.\n- **Best for content creation**: **Kingston Fury Beast DDR5-6000 (32GB)** for high capacity.\n- **Best for competitive gaming**: **TeamGroup T-Force XTREEM DDR4-3600 (16GB)** for low latency.\n\nAlways check motherboard compatibility (QVL list) and ensure proper cooling for high-speed RAM. If you have a specific budget or use case, let me know for more tailored recommendations!'
                    ]
                else:
                    mock_responses = [
                        'Here is a balanced gaming PC build for your $1500 budget:\n\nCPU: AMD Ryzen 5 7600X - $240\nGPU: NVIDIA GeForce RTX 4060 Ti - $350\nMotherboard: MSI MAG B550 TOMAHAWK WIFI - $160\nRAM: Corsair Vengeance 16GB DDR5-5600 - $75\nStorage: Samsung 970 EVO Plus 1TB NVMe SSD - $80\nPSU: EVGA SuperNOVA 650 G5 80 Plus Gold - $100\nCase: NZXT H510 - $80\nCooling: Cooler Master Hyper 212 Black Edition - $40\n\nTotal Cost: $1125',
                        'High-performance gaming PC for $2000 budget:\n\nCPU: AMD Ryzen 7 7700X - $350\nGPU: NVIDIA GeForce RTX 4070 Ti - $600\nMotherboard: ASUS ROG STRIX B650-A GAMING WIFI - $250\nRAM: G.Skill Ripjaws V 32GB DDR5-6000 - $120\nStorage: Samsung 980 PRO 2TB NVMe SSD - $150\nPSU: Corsair RM750x 80 Plus Gold - $130\nCase: Lian Li PC-O11 Dynamic - $150\nCooling: NZXT Kraken X63 AIO - $120\n\nTotal Cost: $1870',
                        'Budget gaming PC for $1000 budget:\n\nCPU: AMD Ryzen 5 5600 - $120\nGPU: NVIDIA GeForce RTX 4060 - $280\nMotherboard: MSI B450 TOMAHAWK MAX - $90\nRAM: Corsair Vengeance LPX 16GB DDR4-3200 - $50\nStorage: Crucial P5 Plus 1TB NVMe SSD - $70\nPSU: EVGA BR 600 W1 80 Plus Bronze - $50\nCase: Cooler Master MasterBox NR400 - $60\nCooling: Stock AMD Wraith Stealth - $0\n\nTotal Cost: $720',
                        'Content creation workstation for $1800 budget:\n\nCPU: AMD Ryzen 7 7700X - $350\nGPU: NVIDIA GeForce RTX 4060 Ti - $400\nMotherboard: ASUS TUF GAMING B650-PLUS WIFI - $180\nRAM: Corsair Vengeance 32GB DDR5-5600 - $110\nStorage: Samsung 980 PRO 1TB NVMe SSD - $90\nPSU: Seasonic Focus GX-650 80 Plus Gold - $90\nCase: Fractal Design Define 7 - $120\nCooling: be quiet! Dark Rock Pro 4 - $80\n\nTotal Cost: $1420',
                        'Ultra-budget PC for $600 budget:\n\nCPU: AMD Ryzen 5 5600G - $140\nGPU: Integrated Radeon Graphics - $0\nMotherboard: ASRock B450M PRO4 - $60\nRAM: Crucial 16GB DDR4-3200 - $45\nStorage: Kingston NV2 500GB NVMe SSD - $35\nPSU: EVGA 500 W1 80 Plus White - $35\nCase: Cooler Master MasterBox Q300L - $40\nCooling: Stock AMD Wraith Stealth - $0\n\nTotal Cost: $355',
                        'Premium gaming PC for $2500 budget:\n\nCPU: Intel Core i7-13700K - $450\nGPU: NVIDIA GeForce RTX 4070 Ti SUPER - $700\nMotherboard: ASUS ROG STRIX Z690-A GAMING WIFI D4 - $300\nRAM: G.Skill Trident Z5 RGB 32GB DDR5-6000 - $160\nStorage: Samsung 990 PRO 2TB NVMe SSD - $180\nPSU: Corsair RM850x 80 Plus Gold - $150\nCase: Lian Li PC-O11D XL ROG Certified - $180\nCooling: Corsair H170i ELITE CAPELLIX AIO - $180\n\nTotal Cost: $2300',
                        'Entry-level gaming PC for $800 budget:\n\nCPU: Intel Core i3-12100F - $100\nGPU: NVIDIA GeForce GTX 1650 - $150\nMotherboard: MSI H510M-A PRO - $70\nRAM: Kingston HyperX 16GB DDR4-3200 - $55\nStorage: WD Blue SN570 500GB NVMe SSD - $45\nPSU: Thermaltake Smart 500W 80 Plus White - $40\nCase: Cooler Master MasterBox MB311L - $50\nCooling: Intel Stock Cooler - $0\n\nTotal Cost: $510',
                        'Mid-range gaming PC for $1200 budget:\n\nCPU: AMD Ryzen 5 7600 - $200\nGPU: NVIDIA GeForce RTX 4060 Ti - $350\nMotherboard: Gigabyte B650 AORUS ELITE AX - $140\nRAM: TeamGroup T-Force Vulcan 16GB DDR5-5200 - $65\nStorage: Crucial P5 1TB NVMe SSD - $75\nPSU: Corsair CX550M 80 Plus Bronze - $70\nCase: NZXT H5 - $90\nCooling: AMD Wraith Prism - $30\n\nTotal Cost: $1020',
                        'High-end workstation for $2200 budget:\n\nCPU: Intel Core i9-13900K - $600\nGPU: NVIDIA GeForce RTX 4070 SUPER - $650\nMotherboard: ASUS PRIME Z790-A WIFI - $350\nRAM: Corsair Dominator Platinum 32GB DDR5-6200 - $180\nStorage: Samsung 980 PRO 2TB NVMe SSD - $150\nPSU: EVGA SuperNOVA 850 GT 80 Plus Gold - $140\nCase: be quiet! Dark Base 700 - $160\nCooling: NZXT Kraken Z73 AIO - $150\n\nTotal Cost: $2380',
                        'Budget streaming PC for $900 budget:\n\nCPU: AMD Ryzen 5 5600X - $150\nGPU: NVIDIA GeForce RTX 3050 - $200\nMotherboard: ASRock B550M PRO4 - $80\nRAM: G.Skill Aegis 16GB DDR4-3600 - $60\nStorage: Samsung 870 EVO 1TB SATA SSD - $80\nPSU: Cooler Master MWE 550 Bronze V2 - $60\nCase: Fractal Design Core 1000 - $70\nCooling: Cooler Master Hyper H412R - $35\n\nTotal Cost: $735',
                        'Compact gaming PC for $1300 budget:\n\nCPU: Intel Core i5-13600KF - $250\nGPU: NVIDIA GeForce RTX 4060 - $300\nMotherboard: MSI MAG B660 TOMAHAWK WIFI DDR4 - $130\nRAM: Corsair Vengeance LPX 16GB DDR4-3600 - $65\nStorage: WD Black SN850X 1TB NVMe SSD - $90\nPSU: Seasonic S12III 550 80 Plus Bronze - $65\nCase: Cooler Master NR200P - $100\nCooling: Noctua NH-U12S - $70\n\nTotal Cost: $1070',
                        'Future-proof gaming PC for $2800 budget:\n\nCPU: AMD Ryzen 9 7950X - $700\nGPU: NVIDIA GeForce RTX 4080 SUPER - $1000\nMotherboard: ASUS ROG CROSSHAIR X670E EXTREME - $600\nRAM: G.Skill Trident Z5 RGB 64GB DDR5-6400 - $300\nStorage: Samsung 990 PRO 4TB NVMe SSD - $400\nPSU: Corsair AX1000 80 Plus Titanium - $200\nCase: Lian Li PC-O11D XL - $180\nCooling: Corsair H170i ELITE CAPELLIX AIO - $180\n\nTotal Cost: $3560'
                    ]
                import random
                ai_response = random.choice(mock_responses)
                return jsonify({"success": True, "response": ai_response})
            else:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                system_prompt = "You are an expert PC builder assistant. Help users design custom PCs by recommending compatible components (CPU, GPU, motherboard, RAM, storage, PSU, case, cooling) based on their budget, intended use (e.g., gaming, work, streaming), preferences, and any specific requirements. Provide detailed explanations, compatibility checks, and total cost estimates. If needed, suggest optimizations or alternatives."
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # or gpt-4 if available
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content.strip()
                
                return jsonify({"success": True, "response": ai_response})
        
        except Exception as e:
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    @app.route('/api/auth/me')
    def api_auth_me():
        info = session.get('user_info')
        if not info:
            return jsonify({"authenticated": False}), 401
        return jsonify({"authenticated": True, "user": info})
    
    @app.route('/forgot-password', methods=['POST'])
    def forgot_password():
        data = request.get_json()
        email = data.get('email')
        
        # In a real application, you would verify the email exists
        # and send a password reset link
        
        return jsonify({
            "message": "If your email exists in our system, you will receive a password reset link",
            "success": True
        })
    
    @app.route('/google-login', methods=['POST'])
    def google_login():
        # In a real application, you would handle Google OAuth here
        # This is just a placeholder
        return jsonify({
            "message": "Google login endpoint",
            "error": "Implementation would require Google OAuth credentials"
        })
    
    return app

app = create_app()

# 初始化数据库
with app.app_context():
    db.create_all()
    
    # 创建示例数据
    if not User.query.first():
        # 创建示例用户
        users_data = [
            {'username': '张先生', 'email': 'zhang@example.com', 'password': 'password123', 'location': '沙田'},
            {'username': '李女士', 'email': 'li@example.com', 'password': 'password123', 'location': '旺角'},
            {'username': '王先生', 'email': 'wang@example.com', 'password': 'password123', 'location': '尖沙咀'},
            {'username': '陈先生', 'email': 'chen@example.com', 'password': 'password123', 'location': '佐敦'},
            {'username': '刘女士', 'email': 'liu@example.com', 'password': 'password123', 'location': '荃湾'},
            {'username': '黄先生', 'email': 'huang@example.com', 'password': 'password123', 'location': '九龙湾'},
            {'username': '林先生', 'email': 'lin@example.com', 'password': 'password123', 'location': '中环'},
            {'username': '陈女士', 'email': 'chen2@example.com', 'password': 'password123', 'location': '铜锣湾'}
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                location=user_data['location'],
                rating=4.5 + (hash(user_data['username']) % 10) / 20,  # 4.5-5.0之间的评分
                sales_count=hash(user_data['username']) % 500  # 0-499之间的销量
            )
            db.session.add(user)
        
        # 创建分类
        categories_data = [
            {'name': '手机', 'description': '手机及配件'},
            {'name': '摄影', 'description': '相机及摄影设备'},
            {'name': '电脑', 'description': '电脑及数码产品'},
            {'name': '影音', 'description': '影音设备'},
            {'name': '游戏', 'description': '游戏设备'},
            {'name': '手表', 'description': '手表及配件'},
            {'name': '汽车', 'description': '汽车用品'},
            {'name': '电器', 'description': '家用电器'}
        ]
        
        for cat_data in categories_data:
            category = Category(name=cat_data['name'], description=cat_data['description'])
            db.session.add(category)
        
        db.session.commit()
        
        # 创建示例商品
        products_data = [
            {
                'name': 'iPhone 13 128GB 蓝色 99新',
                'description': '有盒子,冇花冇壞,購自Apple store',
                'price': 2680,
                'original_price': 3200,
                'condition': '99新',
                'brand': 'Apple',
                'location': '沙田',
                'images': '["https://via.placeholder.com/300x200/007AFF/FFFFFF?text=iPhone+13"]',
                'tags': '["包邮", "支持验货", "7天退换"]',
                'category_id': 1,  # 手机
                'seller_id': 1
            },
            {
                'name': 'Sony A6400 微单相机 套机',
                'description': '功能正常无拆修,运行流畅拍照清晰',
                'price': 3500,
                'original_price': 4200,
                'condition': '95新',
                'brand': 'Sony',
                'location': '旺角',
                'images': '["https://via.placeholder.com/300x200/FF6B35/FFFFFF?text=A6400"]',
                'tags': '["包邮", "专业设备", "1年保修"]',
                'category_id': 2,  # 摄影
                'seller_id': 2
            },
            {
                'name': 'Google Pixel 7 128GB 黑色',
                'description': '几乎全新,屏幕有维修记录',
                'price': 2000,
                'original_price': 2800,
                'condition': '9成新',
                'brand': 'Google',
                'location': '尖沙咀',
                'images': '["https://via.placeholder.com/300x200/4285F4/FFFFFF?text=Pixel+7"]',
                'tags': '["包邮", "可小刀", "支持验货"]',
                'category_id': 1,  # 手机
                'seller_id': 3
            },
            {
                'name': 'Canon 24-70mm F2.8L II 镜头',
                'description': '专业镜头,成色新,功能正常',
                'price': 5200,
                'original_price': 6800,
                'condition': '98新',
                'brand': 'Canon',
                'location': '佐敦',
                'images': '["https://via.placeholder.com/300x200/FF0000/FFFFFF?text=24-70+F2.8"]',
                'tags': '["包邮", "专业设备", "支持验货"]',
                'category_id': 2,  # 摄影
                'seller_id': 4
            },
            {
                'name': 'AirPods Pro 2代 降噪耳机',
                'description': '全新未拆封,正品保证',
                'price': 980,
                'original_price': 1200,
                'condition': '全新',
                'brand': 'Apple',
                'location': '荃湾',
                'images': '["https://via.placeholder.com/300x200/000000/FFFFFF?text=AirPods+Pro"]',
                'tags': '["包邮", "全新", "正品保证"]',
                'category_id': 4,  # 影音
                'seller_id': 5,
                'is_new': True
            },
            {
                'name': 'Sony PS5 游戏主机 光驱版',
                'description': '功能正常,配件齐全,成色新',
                'price': 2980,
                'original_price': 3800,
                'condition': '9成新',
                'brand': 'Sony',
                'location': '九龙湾',
                'images': '["https://via.placeholder.com/300x200/003791/FFFFFF?text=PS5"]',
                'tags': '["包邮", "热门商品", "配件齐全"]',
                'category_id': 5,  # 游戏
                'seller_id': 6
            },
            {
                'name': 'MacBook Pro 13寸 M1芯片 256GB',
                'description': 'M1芯片,性能强劲,成色新',
                'price': 6800,
                'original_price': 8500,
                'condition': '95新',
                'brand': 'Apple',
                'location': '中环',
                'images': '["https://via.placeholder.com/300x200/000000/FFFFFF?text=MacBook+Pro"]',
                'tags': '["包邮", "高端设备", "支持验货"]',
                'category_id': 3,  # 电脑
                'seller_id': 7
            },
            {
                'name': 'Nintendo Switch OLED 白色',
                'description': 'OLED屏幕,成色新,配件齐全',
                'price': 1800,
                'original_price': 2200,
                'condition': '9成新',
                'brand': 'Nintendo',
                'location': '铜锣湾',
                'images': '["https://via.placeholder.com/300x200/FF0000/FFFFFF?text=Switch+OLED"]',
                'tags': '["包邮", "游戏设备", "配件齐全"]',
                'category_id': 5,  # 游戏
                'seller_id': 8
            }
        ]
        
        for prod_data in products_data:
            product = Product(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                original_price=prod_data['original_price'],
                condition=prod_data['condition'],
                brand=prod_data['brand'],
                location=prod_data['location'],
                images=prod_data['images'],
                tags=prod_data['tags'],
                category_id=prod_data['category_id'],
                seller_id=prod_data['seller_id'],
                is_new=prod_data.get('is_new', False),
                views=hash(prod_data['name']) % 500,
                favorites=hash(prod_data['name']) % 100
            )
            db.session.add(product)
        
        db.session.commit()
        print("数据库初始化完成！")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)