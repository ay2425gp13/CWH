@echo off
chcp 65001 >nul
echo ========================================
echo     启动 Flask 服务器
echo ========================================
echo.

cd /d "%~dp0backend"

echo 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo 正在检查虚拟环境...
if not exist ".venv" (
    echo 虚拟环境不存在，正在创建...
    python -m venv .venv
    echo 虚拟环境创建完成！
)

echo 正在激活虚拟环境...
call .venv\Scripts\activate.bat

echo 正在检查并安装依赖...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo     服务器正在启动...
echo ========================================
echo.
echo 服务器地址: http://127.0.0.1:5000
echo 登录页面: http://127.0.0.1:5000/login
echo.
echo 按 Ctrl+C 可以停止服务器
echo.

start http://127.0.0.1:5000/login

python app.py

pause










