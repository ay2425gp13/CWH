How to Start the Server and Open Web Pages
Method 1: Use Batch Script (Easiest)
Double-click the Start Server.bat file in the project root folder. It will:
Automatically create a virtual environment (if it doesn't exist)
Install required dependencies
Start the Flask server
Open the login page in your browser automatically
Method 2: Start Manually in CMD
Step 1: Open CMD
Press Win + R, type cmd, and press Enter
Step 2: Navigate to the Project Folder
cmd
cd /d E:\ITP4506\backend
Step 3: Create and Activate Virtual Environment (First Run)
cmd
python -m venv .venv
.venv\Scripts\activate.bat
If you get an execution policy error:
Run PowerShell as administrator once
Run this command:
powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
Step 4: Install Dependencies (First Run or After Updates)
cmd
pip install -r requirements.txt
Step 5: Start the Server
cmd
python app.py
Step 6: Open Web Pages
After the server starts, you'll see a message like this:
plaintext
 * Running on http://0.0.0.0:5000
Open any of these addresses in your browser:
Login Page: http://127.0.0.1:5000/login
Home Page: http://127.0.0.1:5000
API Status: http://127.0.0.1:5000/api
Or run this command directly in CMD:
cmd
start http://127.0.0.1:5000/login
Other Available Pages
Once the server is running, you can visit these pages:
Login: http://127.0.0.1:5000/login
Signup: http://127.0.0.1:5000/signup
Platform Market: http://127.0.0.1:5000/platform-market.html
Customer Menu: http://127.0.0.1:5000/menu
My Items: http://127.0.0.1:5000/my-items
My Reviews: http://127.0.0.1:5000/my-reviews
My Favorites: http://127.0.0.1:5000/my-favorites
Stop the Server
Press Ctrl + C in the CMD window where the server is running.
Common Issues
1. Port 5000 Is Already in Use
If you see a "port occupied" error, change the port number in the last line of backend/app.py:
python
运行
app.run(debug=True, host='0.0.0.0', port=5001)  # Use another port
2. "Module Not Found" Error
Make sure the virtual environment is activated and all dependencies are installed:
cmd
.venv\Scripts\activate.bat
pip install -r requirements.txt
3. Database Errors
The database file is automatically created at backend/instance/marketplace.db. If you have issues:
Delete this file
Restart the server to let the system create a new one







