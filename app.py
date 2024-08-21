from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)
a = ['sharavanask', 'saravananbs', 'siva2394', 'sheiknaveedh']

@app.route('/', methods=['GET'])
def user_info():
    b = {}

    for handle in a:
        # Fetch user info
        user_info_url = f'https://codeforces.com/api/user.info?handles={handle}'
        user_info_response = requests.get(user_info_url)

        # Fetch user contest history
        contest_history_url = f'https://codeforces.com/api/user.rating?handle={handle}'
        contest_history_response = requests.get(contest_history_url)

        if user_info_response.status_code == 200 and contest_history_response.status_code == 200:
            user_data = user_info_response.json()['result'][0]

            # Get the last contest
            contest_history = contest_history_response.json()['result']
            if contest_history:
                last_contest = contest_history[-1]

                # Fetch the user's submissions in the last contest
                contest_id = last_contest['contestId']
                submissions_url = f'https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000'
                submissions_response = requests.get(submissions_url)
                if submissions_response.status_code == 200:
                    submissions = submissions_response.json()['result']
                    problems_solved = set()

                    for submission in submissions:
                        if submission['contestId'] == contest_id and submission['verdict'] == 'OK':
                            problem_id = (submission['problem']['contestId'], submission['problem']['index'])
                            problems_solved.add(problem_id)

                    # Add the number of problems solved in the last contest
                    user_data['last_contest'] = {
                        'contestId': contest_id,
                        'contestName': last_contest['contestName'],
                        'problems_solved': len(problems_solved)
                    }
            else:
                user_data['last_contest'] = None

            b[handle] = user_data
        else:
            return jsonify({'error': 'Failed to fetch user info or contest history'}), user_info_response.status_code

    return render_template('index.html', user_data=b)

# Custom Jinja2 filter to format timestamps
@app.template_filter('to_datetime')
def to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app.run(debug=True)
