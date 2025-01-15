# This is a sample Python app in flask quickstart
# This is a simple app that returns "Hello World!" to the browser
# The app runs on port 5000

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
