from flask import Flask, jsonify, request,render_template
import requests
from datetime import datetime
app = Flask(__name__)
a=['sharavanask','saravananbs','siva2394']

@app.route('/', methods=['GET'])
def user_info():
    b={}
    # URL of the Codeforces API endpoint for user info
    for i in a:
        api_url = f'https://codeforces.com/api/user.info?handles={i}'

    # Send a GET request to the Codeforces API
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON data from the API
            b[i]=response.json()
        else:
            # Handle errors or non-successful responses
            return jsonify({'error': 'Failed to fetch user info'}), response.status_code
    # return jsonify(b)
    return render_template('index.html', user_data=b)

# Custom Jinja2 filter to format timestamps
@app.template_filter('to_datetime')
def to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app.run(debug=True)