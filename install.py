import launch
import sys

# List of dependencies and their specific versions
dependencies = {
    "Pillow": "9.1.0",
    "gradio": "", 
}
# Function to check and install dependencies
def install_dependencies(deps):
    for package, version in deps.items():
        package_name = f"{package}=={version}" if version else package
        try:
            if not launch.is_installed(package_name):
                print(f"Installing {package_name}...")
                launch.run_pip(f"install {package_name}", f"requirements for Multi-Prompt Manager")
            else:
                print(f"{package_name} is already installed.")
        except Exception as e:
            print(f"Failed to install {package_name}: {e}")
            print("Please check your permissions and try running the script with elevated privileges.")
            sys.exit(1)

# Install dependencies
install_dependencies(dependencies)

print("All dependencies are installed.")
