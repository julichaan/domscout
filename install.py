import shutil
import subprocess
import sys
import platform
import os

TOOLS = [
    "subfinder",
    "findomain",
    "assetfinder",
    "sublist3r",
    "httpx",
    "gowitness",
    "curl",
    "jq"
]

def check_tool(tool):
    """Check if a tool is available in the system PATH."""
    return shutil.which(tool) is not None

def install_brew_tool(package_name):
    """Install a tool using Homebrew on macOS."""
    print(f"[*] Installing {package_name} via Homebrew...")
    try:
        subprocess.run(["brew", "install", package_name], check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Failed to install {package_name} with brew. Trying to tap projectdiscovery if applicable...")
        if package_name in ["subfinder", "httpx"]:
             subprocess.run(["brew", "tap", "projectdiscovery/tap"], check=False)
             subprocess.run(["brew", "install", f"projectdiscovery/tap/{package_name}"], check=False)

def install_apt_tool(package_name):
    """Install a tool using apt on Linux."""
    print(f"[*] Installing {package_name} via apt...")
    subprocess.run(["sudo", "apt", "update"], check=False)
    subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)

def install_go_tool(package_url, binary_name):
    """Install a tool using Go."""
    print(f"[*] Installing {binary_name} via Go...")
    try:
        subprocess.run(["go", "install", package_url], check=True)
        
        # Check if GOPATH/bin is in PATH
        home = os.path.expanduser("~")
        go_bin = os.path.join(home, "go", "bin")
        if go_bin not in os.environ["PATH"]:
            print(f"[!] Warning: {go_bin} is not in your PATH. You may need to add it to run {binary_name}.")
            print(f"    export PATH=$PATH:{go_bin}")
    except Exception as e:
        print(f"[!] Failed to install {binary_name} via Go: {e}")

def install_pip_tool(package_name):
    """Install a tool using pip."""
    print(f"[*] Installing {package_name} via pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)

def install_linux_binary(url, binary_name):
    """Download and install a binary on Linux."""
    print(f"[*] Downloading binary for {binary_name}...")
    try:
        subprocess.run(f"curl -L -o {binary_name}.zip {url}", shell=True, check=True)
        subprocess.run(f"unzip -o {binary_name}.zip", shell=True, check=True)
        subprocess.run(f"chmod +x {binary_name}", shell=True, check=True)
        subprocess.run(f"sudo mv {binary_name} /usr/local/bin/", shell=True, check=True)
        subprocess.run(f"rm {binary_name}.zip", shell=True, check=False)
        print(f"[+] {binary_name} installed successfully.")
    except Exception as e:
        print(f"[!] Failed to install {binary_name}: {e}")

def install_chrome_linux():
    """Download and install Google Chrome on Linux."""
    print("[*] Downloading and installing Google Chrome...")
    try:
        subprocess.run("curl -L -o google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True, check=True)
        subprocess.run("sudo apt install -y ./google-chrome.deb", shell=True, check=True)
        subprocess.run("rm google-chrome.deb", shell=True, check=False)
        print("[+] Google Chrome installed successfully.")
    except Exception as e:
        print(f"[!] Failed to install Google Chrome: {e}")
        print("    [!] Recommendation: Please install Google Chrome manually from https://www.google.com/chrome/")

def install_chrome_mac():
    """Install Google Chrome on macOS via Homebrew."""
    print("[*] Installing Google Chrome via Homebrew...")
    try:
        subprocess.run(["brew", "install", "--cask", "google-chrome"], check=True)
        print("[+] Google Chrome installed successfully.")
    except subprocess.CalledProcessError:
        print("[!] Failed to install Google Chrome via Homebrew.")
        print("    [!] Recommendation: Run 'brew install --cask google-chrome' or install manually from https://www.google.com/chrome/")
        print("    [!] Important: Ensure the application is located at '/Applications/Google Chrome.app' so gowitness can find it.")

def main():
    system = platform.system()
    print(f"[*] Detected OS: {system}")

    if system == "Darwin":
        # macOS Installation
        if not check_tool("brew"):
            print("[!] Homebrew not found. Please install Homebrew first: https://brew.sh/")
            sys.exit(1)
        
        for tool in TOOLS:
            if check_tool(tool):
                print(f"[+] {tool} is already installed.")
                continue
            
            if tool in ["subfinder", "assetfinder", "httpx", "findomain", "curl", "jq", "gowitness"]:
                try:
                    install_brew_tool(tool)
                except Exception as e:
                    print(f"[!] Error installing {tool}: {e}")
            elif tool == "sublist3r":
                try:
                    install_pip_tool("sublist3r")
                except Exception as e:
                    print(f"[!] Error installing {tool}: {e}")

        # Check for Google Chrome (required for gowitness)
        print("\n[*] Checking for Google Chrome (required for gowitness)...")
        chrome_paths = [
            "/Applications/Google Chrome.app",
            os.path.expanduser("~/Applications/Google Chrome.app")
        ]
        chrome_found = any(os.path.exists(p) for p in chrome_paths)

        if chrome_found:
             print("[+] Google Chrome is already installed.")
        else:
             install_chrome_mac()
        
        # Create symlink for google-chrome command on macOS
        chrome_app_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        target_link = "/usr/local/bin/google-chrome"
        if os.path.exists(chrome_app_path) and not os.path.exists(target_link):
            print(f"[*] Creating symlink for 'google-chrome' command...")
            try:
                subprocess.run(f"sudo ln -s '{chrome_app_path}' '{target_link}'", shell=True, check=False)
                print("[+] Symlink created at /usr/local/bin/google-chrome")
            except Exception:
                print("[!] Could not create symlink (sudo might be required). Skipping.")

    elif system == "Linux":
        # Linux Installation
        has_apt = check_tool("apt")
        has_go = check_tool("go")

        for tool in TOOLS:
            if check_tool(tool):
                print(f"[+] {tool} is already installed.")
                continue

            if tool in ["curl", "jq"]:
                if has_apt:
                    try:
                        install_apt_tool(tool)
                    except:
                        print(f"[!] Failed to install {tool} via apt.")
                else:
                    print(f"[!] Package manager not supported. Please install {tool} manually.")
            
            elif tool == "sublist3r":
                try:
                    install_pip_tool("sublist3r")
                except:
                    print(f"[!] Failed to install {tool} via pip.")

            elif tool == "findomain":
                # Try to install findomain binary
                # Note: This URL is for x86_64 Linux. 
                url = "https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip"
                install_linux_binary(url, "findomain")

            elif tool in ["subfinder", "assetfinder", "httpx", "gowitness"]:
                if has_go:
                    url = ""
                    if tool == "subfinder": url = "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
                    if tool == "assetfinder": url = "github.com/tomnomnom/assetfinder@latest"
                    if tool == "httpx": url = "github.com/projectdiscovery/httpx/cmd/httpx@latest"
                    if tool == "gowitness": url = "github.com/sensepost/gowitness@latest"
                    install_go_tool(url, tool)
                else:
                    print(f"[!] Go is not installed. Cannot install {tool} automatically via Go.")
                    print(f"    Please install Go (https://go.dev/doc/install) or download the {tool} binary manually.")

        # Check for Google Chrome (required for gowitness)
        print("\n[*] Checking for Google Chrome (required for gowitness)...")
        if check_tool("google-chrome") or check_tool("google-chrome-stable"):
             print("[+] Google Chrome is already installed.")
        else:
             install_chrome_linux()

    else:
        print(f"[!] Unsupported operating system: {system}. Please install tools manually.")

    print("\n[*] Installation check complete.")

if __name__ == "__main__":
    main()
