import launch

# List of dependencies
dependencies = {
    "Pillow": "9.1.0",
    "contextlib": "",  # No specific version needed
    "gradio": "",      # No specific version needed
}

# Function to check and install dependencies
def install_dependencies(deps):
    print("Running Multi-Prompt Extension requirements installer: ")

    for package, version in deps.items():
        if version:
            package_name = f"{package}=={version}"
        else:
            package_name = package
        if not launch.is_installed(package_name):
            print(f"Installing {package_name}...")
            launch.run_pip(f"install {package_name}", f"requirements for Multi-Prompt Manager")
        else:
            print(f"{package_name} is already installed.")

# Install dependencies
install_dependencies(dependencies)

print("All dependencies are installed.")
