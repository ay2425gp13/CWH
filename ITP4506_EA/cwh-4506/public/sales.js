/**
 * sales.js - 銷售端介面（localStorage 模擬）
 * - 列出所有訂單
 * - 篩選狀態
 * - 查看詳情、更新狀態（Requested → Quoted → Confirmed → Processing → Shipped → Delivered）
 * - 更新持久化到 localStorage，客戶端「追蹤」會讀取最新狀態
 */

const ordersList = document.getElementById('ordersList');
const orderDetail = document.getElementById('orderDetail');
const statusFilter = document.getElementById('statusFilter');

function getOrders(){
  return JSON.parse(localStorage.getItem('orders') || '[]');
}
function saveOrders(orders){
  localStorage.setItem('orders', JSON.stringify(orders));
}

function renderOrders(){
  const filter = statusFilter.value;
  const orders = getOrders().filter(o => !filter || o.status === filter);
  ordersList.innerHTML = '';
  if (!orders.length) { ordersList.innerHTML = '<div class="small muted">無符合的訂單</div>'; return; }
  orders.forEach(o => {
    const row = document.createElement('div');
    row.className = 'list-item';
    row.innerHTML = `
      <div>
        <div><strong>${o.orderId}</strong></div>
        <div class="small muted">${o.customer?.name || ''}</div>
      </div>
      <div style="text-align:right">
        <div>${o.status}</div>
        <div class="small muted">${o.estimatedDelivery}</div>
      </div>
    `;
    row.style.cursor = 'pointer';
    row.addEventListener('click', () => showOrderDetail(o.orderId));
    ordersList.appendChild(row);
  });
}

function showOrderDetail(orderId){
  const o = getOrders().find(x=>x.orderId===orderId);
  if(!o){ orderDetail.textContent = '訂單不存在'; return; }
  orderDetail.innerHTML = `
    <div><strong>${o.orderId}</strong></div>
    <div class="small">狀態：${o.status}</div>
    <div class="small">預計交期：${o.estimatedDelivery}</div>
    <hr/>
    <div><strong>商品</strong></div>
    ${o.items.map(it => `<div class="small">${it.title} x${it.qty} - $${(it.price*it.qty).toFixed(2)}</div>`).join('')}
    <hr/>
    <div><strong>客戶</strong></div>
    <div class="small">${o.customer?.name || ''}</div>
    <div class="small">${o.customer?.addr || ''}</div>
    <hr/>
    <div><strong>歷程</strong></div>
    <ul class="timeline" id="detailTimeline">
      ${['Requested','Quoted','Confirmed','Processing','Shipped','Delivered'].map(st => `
        <li data-status="${st}" class="${st===o.status ? 'active' : ''}">${st}</li>
      `).join('')}
    </ul>
    <div style="display:flex;gap:8px;margin-top:8px">
      <select id="newStatus" class="select">
        <option value="Requested">Requested</option>
        <option value="Quoted">Quoted</option>
        <option value="Confirmed">Confirmed</option>
        <option value="Processing">Processing</option>
        <option value="Shipped">Shipped</option>
        <option value="Delivered">Delivered</option>
      </select>
      <button id="updateStatusBtn" class="btn">更新狀態</button>
    </div>
  `;
  document.getElementById('newStatus').value = o.status;

  document.getElementById('updateStatusBtn').addEventListener('click', ()=>{
    const next = document.getElementById('newStatus').value;
    updateOrderStatus(orderId, next);
  });
}

function updateOrderStatus(orderId, status){
  const orders = getOrders();
  const o = orders.find(x=>x.orderId===orderId);
  if(!o) return;
  o.status = status;
  o.history = o.history || [];
  o.history.push({ status, time: new Date().toISOString(), note: '' });

  // If Quoted → set estimatedDelivery sooner, demo
  if(status === 'Quoted' && o.estimatedDelivery){
    const dt = new Date(o.estimatedDelivery);
    dt.setDate(dt.getDate() - 1);
    o.estimatedDelivery = dt.toISOString().slice(0,10);
  }

  saveOrders(orders);
  renderOrders();
  showOrderDetail(orderId);

  // animate timeline active step
  const active = document.querySelector('#detailTimeline li.active');
  if(active){
    gsap.fromTo(active,{scale:1.06},{scale:1,duration:0.28});
  }

  // Update client latest order display (so index reads latest)
  localStorage.setItem('latest_order_id', orderId);
}

document.getElementById('refreshOrders').addEventListener('click', renderOrders);
statusFilter.addEventListener('change', renderOrders);

// initial
renderOrders();
