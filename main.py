from python_aternos import Client
from flask import Flask, jsonify, url_for
from flask_cors import CORS, cross_origin

aternos = Client.from_credentials('USERNAME', 'PASSWORD')

servs = aternos.list_servers()
server = servs[0]

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
@cross_origin(origin="*")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return links


@app.route("/start")
@cross_origin(origin="*")
def start_server():
    server.start()
    return jsonify({"statusCode": 200})


@app.route("/stop")
@cross_origin(origin="*")
def stop_server():
    server.stop()
    return jsonify({"statusCode": 200})


@app.route("/restart")
@cross_origin(origin="*")
def restart_server():
    server.restart()
    return jsonify({"statusCode": 200})


@app.route("/cancel")
@cross_origin(origin="*")
def cancel_start():
    server.fetch()
    if server.status == "starting":
        server.cancel()
        return jsonify({"statusCode": 200})
    else:
        return jsonify({"statusCode": 501, "message": "Le serveur n'est pas en train de démarrer"})


@app.route("/confirm")
@cross_origin(origin="*")
def confirm_start():
    server.fetch()
    if server.status == "queue":
        server.confirm()
        return jsonify({"statusCode": 200})
    else:
        return jsonify({"statusCode": 501, "message": "Le serveur n'est pas dans une queue"})


@app.route("/status")
@cross_origin(origin="*")
def get_status():
    server.fetch()
    return jsonify({"statusCode": 200, "message": server.status})


@app.route("/serverinfo")
@cross_origin(origin="*")
def get_info():
    server.fetch()

    info = {
        "ramUsedMB": server.ram,
        "playersCount": server.players_count,
        "players_list": server.players_list,
        "slotsLeft": server.slots,
        "version": server.version,
        "port": server.port,
        "motd": server.motd,
        "domain": server.domain,
        "edition": server.edition,
        "address": server.address
    }
    return jsonify({"statusCode": 200, "message": info})


# if __name__ == "__main__":
#     app.run(debug=False, port=1408)
