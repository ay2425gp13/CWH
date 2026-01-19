from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config as config_dict
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime
from models import db, User, Product, Category, Order, Review, Favorite, Watchlist, Notification

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

    # 兼容 /login.html 访问
    @app.route('/login.html')
    def serve_login_page_html():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/css/<path:filename>')
    def serve_css(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'assets'), filename)

    @app.route('/images/<path:filename>')
    def serve_images(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'images'), filename)

    @app.route('/data/<path:filename>')
    def serve_data(filename: str):
        return send_from_directory(os.path.join(frontend_dir, 'data'), filename)

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
        """Backwards compatibility route: serve platform market page."""
        return send_from_directory(frontend_dir, 'platform-market.html')

    @app.route('/platform-market.html')
    def serve_platform_market():
        return send_from_directory(frontend_dir, 'platform-market.html')

    # Staff 后台管理页面
    @app.route('/staff-dashboard')
    def serve_staff_dashboard():
        return send_from_directory(frontend_dir, 'staff-dashboard.html')

    @app.route('/staff-dashboard.html')
    def serve_staff_dashboard_html():
        return send_from_directory(frontend_dir, 'staff-dashboard.html')

    # Staff 补货管理页面
    @app.route('/staff-restock')
    def serve_staff_restock():
        return send_from_directory(frontend_dir, 'staff-restock.html')

    @app.route('/staff-restock.html')
    def serve_staff_restock_html():
        return send_from_directory(frontend_dir, 'staff-restock.html')

    # Staff 报价单页面
    @app.route('/staff-quote')
    def serve_staff_quote():
        return send_from_directory(frontend_dir, 'staff-quote.html')

    @app.route('/staff-quote.html')
    def serve_staff_quote_html():
        return send_from_directory(frontend_dir, 'staff-quote.html')

    # 报价历史页面
    @app.route('/quote-history')
    def serve_quote_history():
        return send_from_directory(frontend_dir, 'quote-history.html')

    @app.route('/quote-history.html')
    def serve_quote_history_html():
        return send_from_directory(frontend_dir, 'quote-history.html')

    @app.route('/cart')
    def serve_cart_page():
        return send_from_directory(frontend_dir, 'cart.html')

    @app.route('/cart.html')
    def serve_cart_page_direct():
        return send_from_directory(frontend_dir, 'cart.html')

    @app.route('/my-orders')
    def serve_my_orders_page():
        return send_from_directory(frontend_dir, 'my-orders.html')

    @app.route('/my-orders.html')
    def serve_my_orders_page_direct():
        return send_from_directory(frontend_dir, 'my-orders.html')

    @app.route('/customize')
    def serve_customize_page():
        return send_from_directory(frontend_dir, 'customize.html')

    @app.route('/customize.html')
    def serve_customize_page_direct():
        return send_from_directory(frontend_dir, 'customize.html')

    @app.route('/wishlist')
    def serve_wishlist_page():
        return send_from_directory(frontend_dir, 'wishlist.html')

    @app.route('/wishlist.html')
    def serve_wishlist_page_direct():
        return send_from_directory(frontend_dir, 'wishlist.html')

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
        # 从 session 中获取已登录用户的基础信息（用于前端展示）
        user_info = session.get('user_info')
        if not user_info:
            return jsonify({"authenticated": False}), 401
        return jsonify({"authenticated": True, "user": user_info})

    @app.route('/api/user/contact', methods=['GET', 'POST'])
    def user_contact():
        """
        获取 / 更新当前登录用户的注册邮箱和绑定手机号。
        - GET  返回当前邮箱和手机号
        - POST 更新邮箱和/或手机号
        """
        session_info = session.get('user_info')
        if not session_info:
            return jsonify({"success": False, "message": "未登录，无法更新联系方式。"}), 401

        user_id = session_info.get('id')
        if not user_id:
            return jsonify({"success": False, "message": "会话中缺少用户信息。"}), 400

        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"success": False, "message": "用户不存在。"}), 404

        if request.method == 'GET':
            return jsonify({
                "success": True,
                "email": user.email,
                "phone": user.phone
            })

        data = request.get_json() or {}
        new_email = (data.get('email') or '').strip()
        new_phone = (data.get('phone') or '').strip()

        if not new_email and not new_phone:
            return jsonify({
                "success": False,
                "message": "请至少填写新的邮箱或手机号。"
            }), 400

        # 简单校验：如果提供了邮箱，必须包含 @
        if new_email and '@' not in new_email:
            return jsonify({
                "success": False,
                "message": "请输入有效的邮箱地址。"
            }), 400

        # 唯一性校验：邮箱 / 手机号不能与其他用户重复
        if new_email:
            exists_email = User.query.filter(
                User.id != user.id,
                User.email == new_email
            ).first()
            if exists_email:
                return jsonify({
                    "success": False,
                    "message": "该邮箱已被其他账号使用，请更换一个。"
                }), 400

        if new_phone:
            exists_phone = User.query.filter(
                User.id != user.id,
                User.phone == new_phone
            ).first()
            if exists_phone:
                return jsonify({
                    "success": False,
                    "message": "该手机号已被其他账号使用，请更换一个。"
                }), 400

        if new_email:
            user.email = new_email
        if new_phone:
            user.phone = new_phone

        db.session.commit()

        # 更新 session 中的邮箱验证状态
        session_info['email_verified'] = bool(user.email)
        session['user_info'] = session_info

        return jsonify({
            "success": True,
            "message": "联系方式已更新。",
            "email": user.email,
            "phone": user.phone
        })

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
        """Backwards compatibility route: serve platform market page."""
        return send_from_directory(frontend_dir, 'platform-market.html')

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
        user_type = data.get('userType') or 'user'  # 'user' or 'staff'
        name = (data.get('name') or '').strip()

        if not username or not email or not password:
            return jsonify({"success": False, "message": "Username, email and password cannot be empty"}), 400

        # 如果是staff，验证名字字段
        if user_type == 'staff' and not name:
            return jsonify({"success": False, "message": "Name is required for staff registration"}), 400

        # 唯一性检查
        existing_user = User.query.filter(
            db.or_(User.username == username, User.email == email)
        ).first()
        if existing_user:
            return jsonify({"success": False, "message": "Username or email already exists"}), 400

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            password_plain=password,  # Store plain text for display purposes
            role=user_type,
            name=name if user_type == 'staff' else None
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
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
            'email_verified': True if user.email else False,
            'role': user.role or 'user',
            'name': user.name or ''
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

    @app.route('/api/auth/me')
    def api_auth_me():
        info = session.get('user_info')
        if not info:
            return jsonify({"authenticated": False}), 401
        return jsonify({"authenticated": True, "user": info})
    
    @app.route('/forgot-password', methods=['POST'])
    def forgot_password():
        """Verify email or phone, return user information if correct."""
        data = request.get_json() or {}
        email = (data.get('email') or '').strip()
        phone = (data.get('phone') or '').strip()

        # Check if email or phone is provided
        if not email and not phone:
            return jsonify({
                "success": False,
                "message": "Please enter either email or phone number."
            }), 400

        user = None
        identifier_label = 'contact information'

        if email:
            identifier_label = 'email'
            user = User.query.filter_by(email=email).first()
        elif phone:
            identifier_label = 'phone number'
            user = User.query.filter_by(phone=phone).first()

        if not user:
            return jsonify({
                "success": False,
                "message": f"The {identifier_label} you entered does not match our records. Please try again."
            }), 400
        
        # Return user information including plain text password for display
        # If password_plain is None, it means this is an old account created before the field was added
        # We cannot recover the password from hash, so we'll prompt user to reset it
        password_display = user.password_plain
        if not password_display:
            # For old accounts, we cannot display the password
            # User needs to reset password to have it stored in plain text
            password_display = "Password reset required (old account)"
        
        return jsonify({
            "success": True,
            "message": f"Account found. Your account information is displayed below.",
            "user": {
                "email": user.email,
                "phone": user.phone or "Not provided",
                "username": user.username,
                "password": password_display,
                "needs_reset": not bool(user.password_plain)  # Flag to indicate if password reset is needed
            }
        })
    
    @app.route('/reset-password', methods=['POST'])
    def reset_password():
        """Reset password from forgot password flow (no login required)."""
        data = request.get_json() or {}
        email = (data.get('email') or '').strip()
        new_password = data.get('newPassword') or ''
        
        if not email or not new_password:
            return jsonify({
                "success": False,
                "message": "Please enter email and new password."
            }), 400
        
        if len(new_password) < 6:
            return jsonify({
                "success": False,
                "message": "New password must be at least 6 characters long."
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found."
            }), 404
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        user.password_plain = new_password  # Store plain text for display purposes
        try:
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Password has been successfully updated."
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": "Failed to update password. Please try again later."
            }), 500
    
    @app.route('/api/user/change-password', methods=['POST'])
    def change_password():
        """Change password interface (requires login)."""
        # Check if user is logged in
        username = session.get('user')
        if not username:
            return jsonify({
                "success": False,
                "message": "Please login first."
            }), 401
        
        data = request.get_json() or {}
        old_password = data.get('oldPassword') or ''
        new_password = data.get('newPassword') or ''
        
        if not old_password or not new_password:
            return jsonify({
                "success": False,
                "message": "Please enter both old password and new password."
            }), 400
        
        if len(new_password) < 6:
            return jsonify({
                "success": False,
                "message": "New password must be at least 6 characters long."
            }), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found."
            }), 404
        
        # Verify old password
        if not check_password_hash(user.password_hash, old_password):
            return jsonify({
                "success": False,
                "message": "Old password is incorrect."
            }), 400
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        user.password_plain = new_password  # Store plain text for display purposes
        try:
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Password has been successfully updated."
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": "Failed to update password. Please try again later."
            }), 500
    
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
    
    # 更新数据库架构：添加 name 和 role 列（如果不存在）
    try:
        import sqlite3
        # 获取数据库路径 - SQLite URI 格式处理
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            # 如果是相对路径，检查 instance 目录
            if not os.path.isabs(db_path):
                instance_path = os.path.join(os.path.dirname(__file__), 'instance', 'marketplace.db')
                if os.path.exists(instance_path):
                    db_path = instance_path
                else:
                    db_path = os.path.join(os.path.dirname(__file__), db_path)
        else:
            db_path = db_uri.replace('sqlite:///', '')
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查现有列
            cursor.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # 添加 name 列（如果不存在）
            if 'name' not in columns:
                print("Adding 'name' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(100)")
                conn.commit()
                print("✓ Added 'name' column")
            
            # 添加 role 列（如果不存在）
            if 'role' not in columns:
                print("Adding 'role' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
                # 更新现有用户的 role
                cursor.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
                conn.commit()
                print("✓ Added 'role' column")
            
            # 添加 password_plain 列（如果不存在）
            if 'password_plain' not in columns:
                print("Adding 'password_plain' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN password_plain VARCHAR(255)")
                conn.commit()
                print("✓ Added 'password_plain' column")
            
            conn.close()
        else:
            print(f"Database file not found at {db_path}, will be created with new schema")
    except Exception as e:
        print(f"Note: Database schema update: {e}")
        import traceback
        traceback.print_exc()
    
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
                password_plain=user_data['password'],  # Store plain text for display purposes
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