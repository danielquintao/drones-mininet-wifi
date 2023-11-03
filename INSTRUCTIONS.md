1. Copy all the python scripts into Mininet-WiFi's VM `~/mininet-wifi` directory

2. Make sure you have `flask` and `requests` pip-installed (install them with sudo)

3. `sudo python fanet.py`

4. Open an xterm window for the `sta1` (master drone) with `xterm sta1` from mininet-wifi terminal,
   then invoke `python master.py sta1`

5. For all the other drones staX in {sta2, ..., sta9} do `py staX.sendCmd("python nodes.py sta1 staX")` directly in mininet CLI.

**NOTE:** The output of client drones is not visible (we disabled outputs) to avoid the logging messages of the
movement server and be able to do the commands in step 5. 
**To revert it, comment the line `log.setLevel(logging.ERROR)` in `fanet.py`.** You will then need one xterm per drone (9 in total).