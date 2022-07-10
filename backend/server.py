from common import *

if len(sys.argv) != 2:
    print('python3 server.py <PORT>')
    exit()

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
app = Flask(__name__, template_folder='.')
CORS(app)

def _read_file(path):
    if not os.path.exists(path): return ''
    return open(path).read()

@app.route("/api/get/config/<key>")
def api_get_config(key):
    try: 
        return _read_file(f'{DIR_CONFIG}/{key}.json')
    except Exception as e:
        print(e); return ''

@app.route("/api/get/data/<contest>/<username>")
def api_get_data(contest, username):
    try:
        return _read_file(f'{DIR_DATA}/{contest}-{username}.json')
    except Exception as e:
        print(e); return ''

thread = get_thread()
thread.start()
print(f'HOST={HOST} PORT={PORT}')
app.run(host=HOST, port=PORT)
stop_thread()