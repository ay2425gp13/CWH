/**
 * server.js
 * Simple Express server with file-based storage (db.json).
 * Not for production. Use a real DB for production.
 */

const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { nanoid } = require('nanoid');

const DB_PATH = path.join(__dirname, 'db.json');
const PORT = process.env.PORT || 3000;

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Utility: read/write DB (synchronous for simplicity)
function readDB() {
  try {
    const raw = fs.readFileSync(DB_PATH, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    return { products: [], users: [], orders: [] };
  }
}
function writeDB(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2), 'utf8');
}

/* -------------------------
   Public API endpoints
   -------------------------*/

// GET /api/products
app.get('/api/products', (req, res) => {
  const db = readDB();
  res.json(db.products || []);
});

// POST /api/login  (simple demo: match email only)
app.post('/api/login', (req, res) => {
  const { email } = req.body;
  if (!email) return res.status(400).json({ error: 'Email required' });
  const db = readDB();
  let user = db.users.find(u => u.email === email);
  if (!user) {
    user = { id: nanoid(8), email, name: email.split('@')[0] };
    db.users.push(user);
    writeDB(db);
  }
  // Return a simple token (demo only)
  res.json({ token: user.id, user });
});

// Wish list endpoints (client-side wishlist stored per user)
app.get('/api/wishlist/:userId', (req, res) => {
  const db = readDB();
  const userId = req.params.userId;
  const user = db.users.find(u => u.id === userId);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user.wishlist || []);
});

app.post('/api/wishlist/:userId', (req, res) => {
  const db = readDB();
  const userId = req.params.userId;
  const { productId, qty = 1, options = {} } = req.body;
  const user = db.users.find(u => u.id === userId);
  if (!user) return res.status(404).json({ error: 'User not found' });

  user.wishlist = user.wishlist || [];
  // Merge by productId + options
  const match = user.wishlist.find(item =>
    item.productId === productId && JSON.stringify(item.options) === JSON.stringify(options)
  );
  if (match) {
    match.qty += qty;
    match.subtotal = match.qty * match.price;
  } else {
    const product = db.products.find(p => p.id === productId);
    if (!product) return res.status(404).json({ error: 'Product not found' });
    const item = {
      id: nanoid(8),
      productId,
      title: product.title,
      price: product.price,
      qty,
      options,
      subtotal: product.price * qty
    };
    user.wishlist.push(item);
  }
  writeDB(db);
  res.json(user.wishlist);
});

app.put('/api/wishlist/:userId/:itemId', (req, res) => {
  const db = readDB();
  const { userId, itemId } = req.params;
  const { qty, options } = req.body;
  const user = db.users.find(u => u.id === userId);
  if (!user) return res.status(404).json({ error: 'User not found' });
  const item = (user.wishlist || []).find(i => i.id === itemId);
  if (!item) return res.status(404).json({ error: 'Item not found' });
  if (qty !== undefined) item.qty = Math.max(1, parseInt(qty, 10));
  if (options !== undefined) item.options = options;
  item.subtotal = item.qty * item.price;
  writeDB(db);
  res.json(item);
});

app.delete('/api/wishlist/:userId/:itemId', (req, res) => {
  const db = readDB();
  const { userId, itemId } = req.params;
  const user = db.users.find(u => u.id === userId);
  if (!user) return res.status(404).json({ error: 'User not found' });
  user.wishlist = (user.wishlist || []).filter(i => i.id !== itemId);
  writeDB(db);
  res.json({ success: true });
});

// Orders
app.post('/api/orders', (req, res) => {
  const db = readDB();
  const { userId, items, customer, paymentMethod } = req.body;
  if (!userId || !items || !items.length) return res.status(400).json({ error: 'Invalid order' });

  const orderId = 'ORD-' + Date.now();
  const total = items.reduce((s, it) => s + (it.price * it.qty), 0);
  const estimatedDelivery = new Date(Date.now() + 7 * 24 * 3600 * 1000).toISOString().slice(0,10); // +7 days demo

  const order = {
    orderId,
    userId,
    items,
    status: 'Requested',
    history: [{ status: 'Requested', time: new Date().toISOString(), note: 'Order requested' }],
    customer,
    paymentMethod,
    estimatedDelivery,
    total
  };
  db.orders = db.orders || [];
  db.orders.push(order);

  // Optionally clear wishlist items that were ordered (demo: not removing)
  writeDB(db);
  res.json(order);
});

app.get('/api/orders/:orderId', (req, res) => {
  const db = readDB();
  const order = (db.orders || []).find(o => o.orderId === req.params.orderId);
  if (!order) return res.status(404).json({ error: 'Order not found' });
  res.json(order);
});

// Sales endpoints: list and update status
app.get('/api/sales/orders', (req, res) => {
  const db = readDB();
  res.json(db.orders || []);
});

app.put('/api/sales/orders/:orderId/status', (req, res) => {
  const db = readDB();
  const { orderId } = req.params;
  const { status, note, estimatedDelivery } = req.body;
  const order = (db.orders || []).find(o => o.orderId === orderId);
  if (!order) return res.status(404).json({ error: 'Order not found' });
  order.status = status;
  order.history = order.history || [];
  order.history.push({ status, time: new Date().toISOString(), note: note || '' });
  if (estimatedDelivery) order.estimatedDelivery = estimatedDelivery;
  writeDB(db);
  res.json(order);
});

/* -------------------------
   Start server
   -------------------------*/
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
