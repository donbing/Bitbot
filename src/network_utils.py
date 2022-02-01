from .configuration.log_decorator import info_log
import socket
import time


def network_connected(hostname="google.com"):
    # 📡 test if internet is available
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2).close()
        return True
    except:
        time.sleep(1)
    return False


@info_log
def wait_for_internet_connection(action):
    connection_error_shown = False
    while not network_connected():
        # 🚫 draw error message if not already drawn
        if not connection_error_shown:
            connection_error_shown = True
            action()
        time.sleep(10)
