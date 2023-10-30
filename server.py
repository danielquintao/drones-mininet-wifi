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
        lat_final = float(request.args.get("latdir"))
        lon_final = float(request.args.get("longdir"))
        final_pos = (lon_final, lat_final, 0.0)
        n = 60
        path_len=n/3
        wait_len = n - path_len 
        if path_len > 0:
            curr_pos = net.get(node).position
            new_vel = ((final_pos[0] - curr_pos[0])/path_len, (final_pos[1] - curr_pos[1])/path_len)
            new_trace = [(curr_pos[0] + k*new_vel[0], curr_pos[1] + k*new_vel[1], 0.0) for k in range(path_len)]
            for i in range(10000):
                new_trace.append(final_pos)
            net.get(node).p = new_trace
        return "Ok", 200 # OK
    
    @app.route('/give-position', methods=['GET'])
    def give_position():
        node = request.args.get("node")
        print(net.get(node).position)
        return {"position": net.get(node).position}, 200 # OK
        

    return app
