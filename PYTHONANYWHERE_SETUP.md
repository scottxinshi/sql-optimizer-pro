
# PythonAnywhere Free Deployment Instructions

## Step 1: Sign up for PythonAnywhere
1. Go to https://www.pythonanywhere.com
2. Click "Create a Beginner account" (FREE)
3. Choose a username and password

## Step 2: Upload Your Files
1. Go to the "Files" tab
2. Create a new directory: sql_optimizer
3. Upload all your project files to this directory

## Step 3: Set up Virtual Environment
1. Go to the "Consoles" tab
2. Start a new Bash console
3. Run these commands:

```bash
cd sql_optimizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Create Web App
1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.8 or higher
5. Set the source code directory to: /home/yourusername/sql_optimizer

## Step 5: Configure WSGI File
1. Click on the WSGI configuration file
2. Replace the content with the passenger_wsgi.py content
3. Update the path to match your username

## Step 6: Reload Web App
1. Click "Reload" button
2. Your app will be available at: https://yourusername.pythonanywhere.com

## Free Tier Limitations:
- 512 MB storage
- 1 web app
- 1 CPU core
- 512 MB RAM
- Perfect for this application!

## Cost: $0/month
