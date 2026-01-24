from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    rating = db.Column(db.Float, default=5.0)
    sales_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关系
    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys='Review.buyer_id', backref='buyer', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.seller_id', backref='seller', lazy=True)

class Category(db.Model):
    """商品分类表"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    products = db.relationship('Product', backref='category', lazy=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

class Product(db.Model):
    """商品表"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    condition = db.Column(db.String(50))  # 全新, 99新, 95新, 9成新等
    brand = db.Column(db.String(100))
    location = db.Column(db.String(100))
    images = db.Column(db.Text)  # JSON字符串存储多张图片
    tags = db.Column(db.Text)  # JSON字符串存储标签
    stock = db.Column(db.Integer, default=1)
    views = db.Column(db.Integer, default=0)
    favorites = db.Column(db.Integer, default=0)
    is_new = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, sold, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # 关系
    orders = db.relationship('Order', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)

class Order(db.Model):
    """订单表"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, delivered, cancelled
    payment_method = db.Column(db.String(50))
    shipping_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # 关系
    reviews = db.relationship('Review', backref='order', lazy=True)

class Review(db.Model):
    """评价表"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5星
    comment = db.Column(db.Text)
    response = db.Column(db.Text)  # 卖家回复
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

class Favorite(db.Model):
    """收藏表"""
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # 唯一约束
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product_favorite'),)

class Watchlist(db.Model):
    """关注列表表"""
    __tablename__ = 'watchlist'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='watchlist_users')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='watchlist_sellers')
    
    # 唯一约束
    __table_args__ = (db.UniqueConstraint('user_id', 'seller_id', name='unique_user_seller_watchlist'),)

class Notification(db.Model):
    """通知表"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.String(50))  # order, message, system等
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Hardware(db.Model):
    """硬件组件表"""
    __tablename__ = 'hardware'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # CPU, GPU, RAM, etc.
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    specs = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SSD(db.Model):
    """SSD存储设备表"""
    __tablename__ = 'ssd'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    capacity = db.Column(db.String(50), nullable=False)
    max_sequential_read = db.Column(db.String(100))
    max_sequential_write = db.Column(db.String(100))
    form_factor = db.Column(db.String(100))
    interface = db.Column(db.String(100))
    price = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PSU(db.Model):
    """电源供应器表"""
    __tablename__ = 'psu'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(100))
    energy_efficiency = db.Column(db.String(100))
    wattage = db.Column(db.String(50))
    modular = db.Column(db.String(50))
    length = db.Column(db.String(50))
    price = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Motherboard(db.Model):
    """主板表"""
    __tablename__ = 'motherboard'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    customer_count = db.Column(db.String(100))
    rating_count = db.Column(db.String(50))
    combo_offer = db.Column(db.String(100))
    socket_type = db.Column(db.String(50))
    form_factor = db.Column(db.String(50))
    memory_max = db.Column(db.String(50))
    memory_slots = db.Column(db.String(50))
    chipset = db.Column(db.String(50))
    price = db.Column(db.String(50))
    product_image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RAM(db.Model):
    """内存表"""
    __tablename__ = 'ram'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    speed = db.Column(db.String(100))
    module = db.Column(db.String(100))
    color = db.Column(db.String(50))
    cas_latency = db.Column(db.String(20))
    price = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GPU(db.Model):
    """显卡表"""
    __tablename__ = 'gpu'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    gpu_model = db.Column(db.String(100))
    memory_size = db.Column(db.String(50))
    cooler_type = db.Column(db.String(50))
    tdp = db.Column(db.String(20))
    price = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CPU(db.Model):
    """CPU处理器表"""
    __tablename__ = 'cpu'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    customer_count = db.Column(db.String(100))
    promotion = db.Column(db.String(500))
    rating_count = db.Column(db.String(50))
    combo_offer = db.Column(db.String(100))
    number_of_cores = db.Column(db.String(50))
    core_clock_speed = db.Column(db.String(50))
    memory_type = db.Column(db.String(50))
    tdp = db.Column(db.String(20))
    integrated_graphics = db.Column(db.String(100))
    price = db.Column(db.String(50))
    product_image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Case(db.Model):
    """机箱表"""
    __tablename__ = 'case'
    
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(100))
    color = db.Column(db.String(50))
    led_type = db.Column(db.String(50))
    case_material = db.Column(db.String(100))
    max_gpu_length = db.Column(db.String(50))
    price = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
