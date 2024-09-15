import subprocess
import os
import yaml
import subprocess
import os
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.utils import create_from_yaml

class K3sManager:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.k3s_script_path = os.path.join(base_path, '..', '..', 'scripts', 'install-k3s.sh')
        self.k3s_config_path = os.path.join(base_path, '..', '..', 'config', 'k3s-config.yaml')
        self.kubeconfig_path = os.path.join(base_path, '..', '..', 'config', 'kubeconfig')

    def is_k3s_installed(self):
        try:
            subprocess.run(["k3s", "--version"], check=True, capture_output=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_k3s(self):
        if self.is_k3s_installed():
            print("K3s is already installed.")
            return

        try:
            subprocess.run(["bash", self.k3s_script_path], check=True, capture_output=True, text=True)
            print("K3s installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install K3s: {e.stderr}")
            raise

    def manage_k3s_service(self, action):
        try:
            subprocess.run(["sudo", "systemctl", action, "k3s"], check=True, capture_output=True, text=True)
            print(f"K3s {action}ed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to {action} K3s: {e.stderr}")
            raise

    def start_k3s(self):
        self.manage_k3s_service("start")

    def stop_k3s(self):
        self.manage_k3s_service("stop")

    def get_cluster_status(self):
        try:
            config.load_kube_config(config_file=self.kubeconfig_path)
            v1 = client.CoreV1Api()
            print("Nodes:")
            for node in v1.list_node().items:
                print(f"- {node.metadata.name}: {node.status.conditions[-1].type}")
            print("\nPods:")
            for pod in v1.list_pod_for_all_namespaces().items:
                print(f"- {pod.metadata.namespace}/{pod.metadata.name}: {pod.status.phase}")
        except ApiException as e:
            print(f"Failed to get cluster status: {e}")
            raise

    def apply_manifest(self, manifest_path):
        try:
            config.load_kube_config(config_file=self.kubeconfig_path)
            create_from_yaml(client.ApiClient(), manifest_path)
            print(f"Applied manifest: {manifest_path}")
        except Exception as e:
            print(f"Failed to apply manifest {manifest_path}: {e}")
            raise

def install():
    manager = K3sManager()
    manager.install_k3s()

def status():
    manager = K3sManager()
    manager.get_cluster_status()

if __name__ == "__main__":
    manager = K3sManager()
    try:
        manager.install_k3s()
        manager.start_k3s()
        manager.get_cluster_status()
    except Exception as e:
        print(f"Failed to execute main: {e}")
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.utils import create_from_yaml

class K3sManager:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.k3s_script_path = os.path.join(base_path, '..', '..', 'scripts', 'install-k3s.sh')
        self.k3s_config_path = os.path.join(base_path, '..', '..', 'config', 'k3s-config.yaml')
        self.kubeconfig_path = os.path.join(base_path, '..', '..', 'config', 'kubeconfig')

    def is_k3s_installed(self):
        try:
            subprocess.run(["k3s", "--version"], check=True, capture_output=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_k3s(self):
        if self.is_k3s_installed():
            print("K3s is already installed.")
            return

        try:
            subprocess.run(["bash", self.k3s_script_path], check=True, capture_output=True, text=True)
            print("K3s installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install K3s: {e.stderr}")

    def manage_k3s_service(self, action):
        try:
            subprocess.run(["sudo", "systemctl", action, "k3s"], check=True, capture_output=True, text=True)
            print(f"K3s {action}ed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to {action} K3s: {e.stderr}")

    def start_k3s(self):
        self.manage_k3s_service("start")

    def stop_k3s(self):
        self.manage_k3s_service("stop")

    def get_cluster_status(self):
        try:
            config.load_kube_config(config_file=self.kubeconfig_path)
            v1 = client.CoreV1Api()
            print("Nodes:")
            for node in v1.list_node().items:
                print(f"- {node.metadata.name}: {node.status.conditions[-1].type}")
            print("\nPods:")
            for pod in v1.list_pod_for_all_namespaces().items:
                print(f"- {pod.metadata.namespace}/{pod.metadata.name}: {pod.status.phase}")
        except ApiException as e:
            print(f"Failed to get cluster status: {e}")

    def apply_manifest(self, manifest_path):
        try:
            config.load_kube_config(config_file=self.kubeconfig_path)
            create_from_yaml(client.ApiClient(), manifest_path)
            print(f"Applied manifest: {manifest_path}")
        except Exception as e:
            print(f"Failed to apply manifest {manifest_path}: {e}")

def install():
    manager = K3sManager()
    manager.install_k3s()

def status():
    manager = K3sManager()
    manager.get_cluster_status()

if __name__ == "__main__":
    manager = K3sManager()
    manager.install_k3s()
    manager.start_k3s()
    manager.get_cluster_status()
