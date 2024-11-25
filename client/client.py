import json
import socket
import requests
from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange


with open("sealpi.json", "r") as f:
    config = json.load(f)

DEVICE_NAME = config["device_name"]
SERVER_TOKEN = config["server_token"]


class SealPiServerDiscovery:
    def __init__(self):
        self.server_host = None
        self.zeroconf = Zeroconf()

    def add_service(self, zeroconf, service_type, name):
        """Callback for when a new service is added."""
        if "sealpi" in name.lower():
            info = zeroconf.get_service_info(service_type, name)
            if info:
                raw_address = socket.inet_ntoa(info.addresses[0])
                print(f"Discovered raw address: {raw_address}")
                port = info.port

                if raw_address == "0.0.0.0":
                    raw_address = "127.0.0.1"
                self.server_host = f"http://{raw_address}:{port}"
                print(f"Resolved Seal-Pi server to: {self.server_host}")
                self.zeroconf.close()

    def discover_server(self):
        """Discover the Seal-Pi server."""
        print("Discovering Seal-Pi server...")
        ServiceBrowser(self.zeroconf, "_http._tcp.local.", self)
        while not self.server_host:
            pass  # Wait for the server to be discovered
        return self.server_host


def register_client(server_host):
    """Register the client with the server."""
    payload = {
        "name": DEVICE_NAME,
        "token": SERVER_TOKEN,
        "ip": socket.gethostbyname(socket.gethostname()),
    }
    print("Registering device with the server...")
    try:
        response = requests.post(f"{server_host}/api/devices/register", json=payload)
        if response.status_code == 200:
            print("Device registered successfully.")
        else:
            print("Device registration failed:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to register device. Exception: {e}")


if __name__ == "__main__":
    discovery = SealPiServerDiscovery()
    server_host = discovery.discover_server()
    register_client(server_host)
