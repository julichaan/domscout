# DomScout

DomScout is a Python-based subdomain enumeration tool for Bug Bounty that aggregates results from multiple powerful tools to provide a comprehensive list of live subdomains for a given target.

## Features

-   **Multi-tool Aggregation**: Combines results from `subfinder`, `findomain`, `assetfinder`, `sublist3r`, and `crt.sh`.
-   **Duplicate Removal**: Automatically merges and deduplicates results from all sources.
-   **Live Subdomain Checking**: Uses `httpx` to verify which subdomains are alive.
-   **Screenshot Capture**: Uses `gowitness` to take screenshots of all live web services.
-   **Progress Tracking**: Displays a real-time progress bar during execution.
-   **Clean Output**: Generates a single file (`alive_subdomains.txt`) with the final results, a `screenshots` folder, and cleans up temporary files.

## Compatibility

-   **Linux**: Fully supported.
-   **macOS**: Fully supported.
-   **Windows**: **Not supported natively**. Windows users must use **WSL (Windows Subsystem for Linux)** to run this tool, as it relies on Unix-specific commands (`sudo`, `sed`, `jq`, `cat`).

## Prerequisites

Before running DomScout, ensure you have the following tools installed and available in your system's PATH:

-   [Python 3](https://www.python.org/)
-   [Subfinder](https://github.com/projectdiscovery/subfinder)
-   [Findomain](https://github.com/Findomain/Findomain)
-   [Assetfinder](https://github.com/tomnomnom/assetfinder)
-   [Sublist3r](https://github.com/aboul3la/Sublist3r)
-   [httpx](https://github.com/projectdiscovery/httpx)
-   [gowitness](https://github.com/sensepost/gowitness)
-   `curl`
-   `jq`

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/julichaan/domscout.git
    cd domscout
    ```

2.  Install dependencies automatically using the provided script:
    ```bash
    python3 install.py
    ```
    
    *Note: The installation script supports macOS (via Homebrew) and Linux (via apt/Go). If you are on another system or prefer manual installation, ensure all tools listed in Prerequisites are installed.*

## Configuration

### Subfinder API Configuration

To get the best results with `subfinder`, it is highly recommended to configure API keys for various services.

1.  Locate the default configuration file for `subfinder`. It is usually located at:
    -   **Linux/macOS**: `$HOME/.config/subfinder/provider-config.yaml`
    -   **Windows**: `%USERPROFILE%\.config\subfinder\provider-config.yaml`

2.  Open the file in a text editor.

3.  Add your API keys in the following format:

    ```yaml
    bevigil: []
	bufferover: []
	builtwith: []
	c99: []
	censys: []
	certspotter: []
	chaos: []
	chinaz: []
	digitalyama: []
	dnsdb: []
	dnsdumpster: []
	dnsrepo: []
	driftnet: []
	facebook: []
	fofa: []
	fullhunt: []
	github: []
	hunter: []
	intelx: []
	leakix: []
	netlas: []
	pugrecon: []
	quake: []
	redhuntlabs: []
	robtex: []
	rsecloud: []
	securitytrails: []
	shodan: []
	threatbook: []
	virustotal: []
	whoisxmlapi: []
	zoomeyeapi: []
    ```

    *Note: You don't need keys for all services, but adding them improves the number of subdomains found.*

## Usage

Run the script using Python 3. You must provide the target domain and the path to a resolvers file.

```bash
python3 domscout.py <target> -r <resolvers_file>
```

### Arguments

-   `target`: The target domain to enumerate (e.g., `example.com`).
-   `-r, --resolvers`: **(Required)** Path to a text file containing DNS resolvers (one per line).
-   `-h, --help`: Show the help message and exit.

### Example

```bash
python3 domscout.py example.com -r /usr/share/wordlists/resolvers.txt
```

### Help

To see all available options:

```bash
python3 domscout.py --help
```

The tool will display a progress bar as it runs through the enumeration steps. Once finished, the live subdomains will be saved in `alive_subdomains.txt`.

## Output

-   **live_subs.txt**: Contains the list of subdomains that successfully resolved via DNS.
-   **alive_webservices.txt**: Contains the list of live web services (HTTP/HTTPS) found by `httpx`.
-   **screenshots/**: Directory containing screenshots of the live web services taken by `gowitness`.

## Author

**julichaan**
