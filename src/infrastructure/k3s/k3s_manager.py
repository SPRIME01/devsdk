import subprocess
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.utils import create_from_yaml


class K3sManager:
    """
    Class to manage K3s clusters.
    """

    def __init__(self, k3s_script_path: str, k3s_config_path: str, kubeconfig_path: str):
        """
        Initialize the K3sManager class.

        Args:
            k3s_script_path (str): Path to the k3s install script.
            k3s_config_path (str): Path to the k3s config file.
            kubeconfig_path (str): Path to the kubeconfig file.
        """
        self.k3s_script_path = k3s_script_path
        self.k3s_config_path = k3s_config_path
        self.kubeconfig_path = kubeconfig_path

    def is_k3s_installed(self) -> bool:
        """
        Check if K3s is installed.

        Returns:
            bool: True if K3s is installed, False otherwise.
        """
        try:
            subprocess.run(["k3s", "--version"], check=True, capture_output=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_k3s(self) -> None:
        """
        Install K3s if it is not installed.
        """
        if self.is_k3s_installed():
            print("K3s is already installed.")
            return

        try:
            subprocess.run(["bash", self.k3s_script_path], check=True, capture_output=True, text=True)
            print("K3s installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install K3s: {e.stderr}")

    def manage_k3s_service(self, action: str) -> None:
        """
        Manage the K3s service.

        Args:
            action (str): The action to perform (start/stop).
        """
        try:
            subprocess.run(["sudo", "systemctl", action, "k3s"], check=True, capture_output=True, text=True)
            print(f"K3s {action}ed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to {action} K3s: {e.stderr}")

    def start_k3s(self) -> None:
        """
        Start the K3s service.
        """
        self.manage_k3s_service("start")

    def stop_k3s(self) -> None:
        """
        Stop the K3s service.
        """
        self.manage_k3s_service("stop")

    def get_cluster_status(self) -> None:
        """
        Get the status of the K3s cluster.
        """
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

    def apply_manifest(self, manifest_path: str) -> None:
        """
        Apply a manifest to the K3s cluster.

        Args:
            manifest_path (str): Path to the manifest file.
        """
        try:
            config.load_kube_config(config_file=self.kubeconfig_path)
            create_from_yaml(client.ApiClient(), manifest_path)
            print(f"Applied manifest: {manifest_path}")
        except Exception as e:
            print(f"Failed to apply manifest {manifest_path}: {e}")


def install() -> None:
    """
    Install K3s if it is not installed.
    """
    manager = K3sManager(k3s_script_path="install-k3s.sh", k3s_config_path="k3s-config.yaml", kubeconfig_path="kubeconfig")
    manager.install_k3s()


def status() -> None:
    """
    Get the status of the K3s cluster.
    """
    manager = K3sManager(k3s_script_path="install-k3s.sh", k3s_config_path="k3s-config.yaml", kubeconfig_path="kubeconfig")
    manager.get_cluster_status()


if __name__ == "__main__":
    manager = K3sManager(k3s_script_path="install-k3s.sh", k3s_config_path="k3s-config.yaml", kubeconfig_path="kubeconfig")
    manager.install_k3s()
    manager.start_k3s()
    manager.get_cluster_status()

