import copy
import subprocess
import uuid

import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return 'OK'

def discover_device(request):
    return {
        'discoveredAppliances': [{
            'actions': [
                'turnOff',
                'turnOn',
            ],
            'applianceId': 'lightberry',
            'manufacturerName': 'Lightberry',
            'modelName': 'Lightberry HD',
            'version': '1',
            'friendlyName': 'Lightberry',
            'friendlyDescription': 'Ambient lighting for TV',
            'isReachable': True,
            'additionalApplianceDetails': {},
        }]
    }

def turn_on(request):
    subprocess.check_output(['hyperion-remote', '-p', '100', '-x'])
    return {}

def turn_off(request):
    subprocess.check_output(['hyperion-remote', '-p', '100', '-c', 'black'])
    return {}

@app.route('/', methods=['POST'])
def main_control():
    request = flask.request.get_json(force=True)
    print(request)
    methods = {
        'DiscoverAppliancesRequest': ('DiscoverAppliancesResponse', discover_device),
        'TurnOnRequest': ('TurnOnConfirmation', turn_on),
        'TurnOffRequest': ('TurnOffConfirmation', turn_off),
    }
    shape, method = methods[request['header']['name']]
    response = method(request['payload'])
    header = copy.deepcopy(request['header'])
    header['messageId'] = str(uuid.uuid4())
    header['name'] = shape
    return flask.jsonify(header=header, payload=response)
