from flask import request, Flask
from src.cms_bluebutton.cms_bluebutton import BlueButton


app = Flask(__name__)
bb = BlueButton()

auth_data = bb.generate_auth_data()

# AuthorizationToken holds access grant info:
# access token, expire in, expire at, token type, scope, refreh token, etc.
# it is associated with current logged in user in real app,
# check SDK python docs for more details.

auth_token = None


@app.route('/api/authorize/authurl', methods=['GET'])
def get_auth_url():
    return bb.generate_authorize_url(auth_data)


@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    code = request_query.get('code')
    state = request_query.get('state')

    auth_token = bb.get_authorization_token(auth_data, code, state)

    config = {
        "auth_token": auth_token,
        "params": {},
        "url": "to be overriden"
    }

    result = {}

    # fetch eob, patient, coverage, profile
    try:
        eob_data = bb.get_explaination_of_benefit_data(config)
        result['eob_data'] = eob_data['response'].json()
        pt_data = bb.get_patient_data(config)
        result['patient_data'] = pt_data['response'].json()
        coverage_data = bb.get_coverage_data(config)
        result['coverage_data'] = coverage_data['response'].json()
        profile_data = bb.get_profile_data(config)
        result['profile_data'] = profile_data['response'].json()
    except Exception as ex:
        print(ex)

    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
