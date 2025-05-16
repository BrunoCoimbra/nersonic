import os

from time import sleep


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOSTS_FILE = os.path.join(ROOT_DIR, "envoy/hosts.txt")
ENDPOINTS_FILE = os.path.join(ROOT_DIR, "envoy/endpoints.yaml")

SLEEP_TIME = 5

DEFAULT_PORTS = [8001, 8011, 8021, 8031]


def update_hosts(hosts: list, ports: list = DEFAULT_PORTS):
    """Generates and writes a YAML file with dynamic endpoint configurations."""

    yaml_content = "resources:\n"
    yaml_content += "- \"@type\": type.googleapis.com/envoy.config.endpoint.v3.ClusterLoadAssignment\n"
    yaml_content += "  cluster_name: nersonic-triton-server\n"
    yaml_content += "  endpoints:\n"
    yaml_content += "  - lb_endpoints:\n"

    for host in hosts:
        for port in ports:
            yaml_content += f"    - endpoint:\n"
            yaml_content += f"        address:\n"
            yaml_content += f"          socket_address:\n"
            yaml_content += f"            address: {host}\n"
            yaml_content += f"            port_value: {port}\n"

    with open(f"{ENDPOINTS_FILE}.tmp", "w") as file:
        file.write(yaml_content)
    os.rename(f"{ENDPOINTS_FILE}.tmp", ENDPOINTS_FILE)


def main():
    hosts = []

    print ("Started endpoint updater")

    while True:
        with open(HOSTS_FILE, "r") as f:
            new_hosts = f.read().splitlines()
        if new_hosts != hosts:
            print(f"Updating hosts: {new_hosts}")
            hosts = new_hosts
            update_hosts(hosts)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
