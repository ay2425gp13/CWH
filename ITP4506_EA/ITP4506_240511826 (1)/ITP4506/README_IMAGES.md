# 玩具图片设置指南

## 方法一：使用Python脚本自动下载（推荐）

### 步骤：

1. **安装依赖**
   ```bash
   pip install requests
   ```

2. **运行脚本**
   ```bash
   python download_toy_images.py
   ```

3. **选择选项1** - 使用Unsplash Source API自动下载图片

   脚本会自动：
   - 根据商品分类下载对应的玩具图片
   - 保存到 `frontend/images/toys/` 目录
   - 自动更新HTML中的图片路径

## 方法二：手动添加图片

### 步骤：

1. **准备图片文件**
   - 图片格式：JPG、PNG
   - 推荐尺寸：280x200 像素
   - 命名格式：`toy_001.jpg`, `toy_002.jpg`, ... (按商品ID)

2. **放置图片**
   - 将图片文件放入 `frontend/images/toys/` 目录

3. **更新图片路径**
   ```bash
   python download_toy_images.py
   ```
   选择选项4 - 更新HTML中的图片路径

## 方法三：使用在线图片URL

### 推荐的免费图片资源：

1. **Unsplash** (https://unsplash.com)
   - 搜索关键词：toy, transformer, action figure, teddy bear 等
   - 免费使用，无需注册（商业使用需注明来源）

2. **Pexels** (https://www.pexels.com)
   - 搜索关键词：toy, children toys, action figure 等
   - 完全免费，包括商业使用

3. **Pixabay** (https://pixabay.com)
   - 搜索关键词：toy, transformer, superhero toy 等
   - 免费使用

### 使用步骤：

1. 访问上述网站，搜索对应的玩具图片
2. 下载图片到 `frontend/images/toys/` 目录
3. 重命名为对应的格式（如 `toy_001.jpg`）
4. 运行脚本更新路径

## 图片命名规则

- 商品ID 1 → `toy_001.jpg`
- 商品ID 2 → `toy_002.jpg`
- 商品ID 10 → `toy_010.jpg`
- 商品ID 100 → `toy_100.jpg`

## 商品分类对应的图片类型

- **变形金刚**: Transformer, Optimus Prime, 机器人玩具
- **玩具枪**: Nerf枪, 水枪, 玩具武器
- **漫威英雄**: 钢铁侠, 蜘蛛侠, 超级英雄手办
- **DC宇宙**: 蝙蝠侠, 超人, DC手办
- **毛绒玩具**: 泰迪熊, 毛绒动物
- **幼儿积木**: 积木, 益智玩具
- **恐龙模型**: 恐龙玩具, 史前动物模型
- **拼图益智**: 拼图, 益智游戏

## 注意事项

1. **版权问题**: 确保使用的图片有合法的使用权限
2. **图片尺寸**: 推荐使用 280x200 像素，保持一致性
3. **文件大小**: 建议每张图片不超过 500KB，优化加载速度
4. **图片格式**: 优先使用 JPG（文件小），PNG（支持透明）

## 故障排除

### 图片不显示？
1. 检查图片文件是否存在于 `frontend/images/toys/` 目录
2. 检查图片路径是否正确（相对路径：`images/toys/toy_001.jpg`）
3. 检查浏览器控制台是否有404错误
4. 确保图片文件权限正确

### 脚本运行错误？
1. 确保已安装 `requests` 库：`pip install requests`
2. 检查网络连接（下载图片需要网络）
3. 如果Unsplash无法访问，使用手动方法添加图片






## 方法一：使用Python脚本自动下载（推荐）

### 步骤：

1. **安装依赖**
   ```bash
   pip install requests
   ```

2. **运行脚本**
   ```bash
   python download_toy_images.py
   ```

3. **选择选项1** - 使用Unsplash Source API自动下载图片

   脚本会自动：
   - 根据商品分类下载对应的玩具图片
   - 保存到 `frontend/images/toys/` 目录
   - 自动更新HTML中的图片路径

## 方法二：手动添加图片

### 步骤：

1. **准备图片文件**
   - 图片格式：JPG、PNG
   - 推荐尺寸：280x200 像素
   - 命名格式：`toy_001.jpg`, `toy_002.jpg`, ... (按商品ID)

2. **放置图片**
   - 将图片文件放入 `frontend/images/toys/` 目录

3. **更新图片路径**
   ```bash
   python download_toy_images.py
   ```
   选择选项4 - 更新HTML中的图片路径

## 方法三：使用在线图片URL

### 推荐的免费图片资源：

1. **Unsplash** (https://unsplash.com)
   - 搜索关键词：toy, transformer, action figure, teddy bear 等
   - 免费使用，无需注册（商业使用需注明来源）

2. **Pexels** (https://www.pexels.com)
   - 搜索关键词：toy, children toys, action figure 等
   - 完全免费，包括商业使用

3. **Pixabay** (https://pixabay.com)
   - 搜索关键词：toy, transformer, superhero toy 等
   - 免费使用

### 使用步骤：

1. 访问上述网站，搜索对应的玩具图片
2. 下载图片到 `frontend/images/toys/` 目录
3. 重命名为对应的格式（如 `toy_001.jpg`）
4. 运行脚本更新路径

## 图片命名规则

- 商品ID 1 → `toy_001.jpg`
- 商品ID 2 → `toy_002.jpg`
- 商品ID 10 → `toy_010.jpg`
- 商品ID 100 → `toy_100.jpg`

## 商品分类对应的图片类型

- **变形金刚**: Transformer, Optimus Prime, 机器人玩具
- **玩具枪**: Nerf枪, 水枪, 玩具武器
- **漫威英雄**: 钢铁侠, 蜘蛛侠, 超级英雄手办
- **DC宇宙**: 蝙蝠侠, 超人, DC手办
- **毛绒玩具**: 泰迪熊, 毛绒动物
- **幼儿积木**: 积木, 益智玩具
- **恐龙模型**: 恐龙玩具, 史前动物模型
- **拼图益智**: 拼图, 益智游戏

## 注意事项

1. **版权问题**: 确保使用的图片有合法的使用权限
2. **图片尺寸**: 推荐使用 280x200 像素，保持一致性
3. **文件大小**: 建议每张图片不超过 500KB，优化加载速度
4. **图片格式**: 优先使用 JPG（文件小），PNG（支持透明）

## 故障排除

### 图片不显示？
1. 检查图片文件是否存在于 `frontend/images/toys/` 目录
2. 检查图片路径是否正确（相对路径：`images/toys/toy_001.jpg`）
3. 检查浏览器控制台是否有404错误
4. 确保图片文件权限正确

### 脚本运行错误？
1. 确保已安装 `requests` 库：`pip install requests`
2. 检查网络连接（下载图片需要网络）
3. 如果Unsplash无法访问，使用手动方法添加图片









