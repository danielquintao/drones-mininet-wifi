import os

from flask import Flask, request


def create_app(net):
    """Creates server to update drones positions on request

    Args:
        net (Mininet_wifi): FANET created with Mininet-WiFi

    Returns:
        Flask: falsk HTTP server
    """
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='csc35'
    )

    @app.route('/update-direction', methods=['GET'])
    def update_direction():
        """Updates direction of a node upon GET request

        Example of request: http://127.0.0.1:5000/update-direction?node=sta1&latdir=1&longdir=1
        """
        node = request.args.get("node")
        latdir = float(request.args.get("latdir"))
        longdir = float(request.args.get("longdir"))
        new_vel = (longdir, latdir)
        n = len(net.get(node).p)
        if n > 0:
            curr_pos = net.get(node).position
            new_trace = [(curr_pos[0] + k*new_vel[0], curr_pos[1] + k*new_vel[1], 0.0) for k in range(n)]
            net.get(node).p = new_trace
        return "Ok", 200 # OK

    return app