import subprocess
def main():
    subprocess.run(['python3', 'manage.py', 'collectstatic', '--noinput'])
    subprocess.run(['python3', 'manage.py', 'makemigrations'])
    subprocess.run(['python3', 'manage.py', 'migrate'])
    subprocess.run(['python3', 'manage.py', 'csu'])
    subprocess.run(['python3', 'manage.py', 'health_check'])
    subprocess.run(['python3', 'manage.py', 'runserver', '127.0.0.1:8000'])

if __name__ == "__main__":
    main()