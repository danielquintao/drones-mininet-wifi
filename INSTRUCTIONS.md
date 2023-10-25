## Branch `explore_drone_control`

1. Copy `fanet.py`, `server.py`, `change_my_dir.py` into Mininet-WiFi's VM `~/mininet-wifi` directory

2. Make sure you have `flask` and `requests` pip-installed (install them with sudo)

3. `sudo python fanet.py`

4. Open an xterm window for the hosts (drones) you want to control (with `xterm <NODE>` from mininet-wifi terminal),
   then invoke `python change_my_dir.py <NODE> <latitude_final> <longitude_final>` as many times as you want to.

5. In open a xterm window to master and run `python master.py sta1` sendo sta1 o nó master. Open another xterm window and run `python master.py sta1 sta2` sendo sta1 nó master e sta2 os nó filho