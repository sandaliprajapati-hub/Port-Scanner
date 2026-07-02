# Port Scanner - Educational Tool

A multi-threaded port scanner with both Command-Line Interface (CLI) and Graphical User Interface (GUI) for educational and authorized security testing purposes.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Screenshots](#screenshots)
4. [Installation](#installation)
5. [Usage](#usage)
   - [Command-Line Interface](#command-line-interface)
   - [Graphical User Interface](#graphical-user-interface)
6. [Architecture](#architecture)
7. [Ethical Use Policy](#ethical-use-policy)
8. [Troubleshooting](#troubleshooting)
9. [License](#license)

---

## Overview

This is a lightweight, educational port scanner built with Python's standard library. It supports:

- **Concurrent port scanning** using `ThreadPoolExecutor`
- **Two interface modes**: CLI and GUI
- **Service detection** for common well-known ports
- **Hostname resolution** via DNS lookup

```
┌─────────────────────────────────────────────────────────────┐
│                    PORT SCANNER ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐      ┌─────────────────┐                 │
│   │  CLI Mode    │  OR  │   GUI Mode      │                 │
│   │  (sys.argv)  │      │   (Tkinter)     │                 │
│   └──────┬───────┘      └────────┬────────┘                 │
│          │                       │                          │
│          └───────────┬───────────┘                          │
│                      ▼                                      │
│          ┌─────────────────────┐                            │
│          │   Main Controller   │                            │
│          │   (resolve_hostname)│                            │
│          └──────────┬──────────┘                            │
│                     ▼                                       │
│          ┌─────────────────────┐                            │
│          │  ThreadPoolExecutor │                            │
│          │  (Concurrent I/O)   │                            │
│          └──────────┬──────────┘                            │
│                     ▼                                       │
│   ┌──────────────────────────────────────────┐              │
│   │         Individual Port Scans            │              │
│   │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │              │
│   │  │ :21 │ │ :22 │ │ :80 │ │ :443│  ...   │              │
│   │  └─────┘ └─────┘ └─────┘ └─────┘        │              │
│   └──────────────────────────────────────────┘              │
│                     │                                       │
│                     ▼                                       │
│          ┌─────────────────────┐                            │
│          │   Results Output    │                            │
│          │   (Open Ports List) │                            │
│          └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-threading** | Configurable thread pool for fast scanning |
| **Service Detection** | Identifies common services (HTTP, SSH, FTP, etc.) |
| **Hostname Resolution** | Resolves domain names to IP addresses |
| **Dual Interface** | CLI for automation, GUI for interactive use |
| **Timeout Control** | Configurable connection timeout per port |
| **Input Validation** | Validates port ranges and parameters |
| **Error Handling** | Graceful handling of network errors |

---

## Screenshots

### GUI Interface Preview

```
┌────────────────────────────────────────────────────────────────┐
│                      Port Scanner - Educational Tool           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Target (IP or Hostname):  [________________________]         │
│                                                                │
│  Start Port:               [________________________]         │
│                                                                │
│  End Port:                 [________________________]         │
│                                                                │
│  Timeout (seconds):        [1.0__________________]            │
│                                                                │
│  Threads:                  [100__________________]            │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ Scanning 192.168.1.1 from port 1 to 100...          │     │
│  │ Resolved 192.168.1.1 to 192.168.1.1                 │     │
│  │                                                      │     │
│  │ Open ports found:                                    │     │
│  │ Port 22: SSH                                         │     │
│  │ Port 80: HTTP                                        │     │
│  │ Port 443: HTTPS                                      │     │
│  │                                                      │     │
│  │ Scan complete. Total ports scanned: 100             │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│              [     Start Scan     ]                           │
│                                                                │
│  ⚠ Use responsibly and only on systems you own or have       │
│    permission to scan.                                        │
└────────────────────────────────────────────────────────────────┘
```

> **📸 Place your GUI screenshot here:**
> 
> ```
![GUI Screenshot]([gui-screenshot.png])
> ```


---

## Installation

### Prerequisites

- **Python 3.6+** (uses `concurrent.futures`, `tkinter`)
- No external dependencies required (standard library only)

### Steps

```bash
# 1. Clone or download the repository
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner

# 2. Verify Python version
python3 --version

# 3. Make the script executable (optional)
chmod +x port_scanner.py

# 4. Run the application
python3 port_scanner.py
```

### Directory Structure

```
port-scanner/
├── port_scanner.py          # Main application file
├── README.md                # This documentation
├── LICENSE                  # License file
└── images/                  # Screenshots directory
    ├── gui-screenshot.png   # <-- Place GUI screenshot here
    └── cli-screenshot.png   # <-- Place CLI screenshot here
```

---

## Usage

### Command-Line Interface

#### Basic Syntax

```bash
python port_scanner.py <target> <start_port> <end_port> [options]
```

#### Positional Arguments

| Argument | Type | Description | Example |
|----------|------|-------------|---------|
| `target` | string | Target IP address or hostname | `192.168.1.1` or `example.com` |
| `start_port` | int | Starting port (inclusive) | `1` |
| `end_port` | int | Ending port (inclusive) | `1024` |

#### Optional Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--timeout` | float | `1.0` | Connection timeout in seconds |
| `--threads` | int | `100` | Number of concurrent threads |

#### Examples

```bash
# Scan common ports on localhost
python port_scanner.py 127.0.0.1 1 1024

# Scan top 1000 ports with higher thread count
python port_scanner.py example.com 1 1000 --threads 200

# Scan with custom timeout (slower but more reliable on unstable networks)
python port_scanner.py 192.168.1.1 1 65535 --timeout 3.0 --threads 50

# Scan specific well-known ports only
python port_scanner.py scanme.nmap.org 20 25 80 443
```

> **Note:** The last example requires slight modification to scan non-contiguous ports. See [Troubleshooting](#troubleshooting).

---

### Graphical User Interface

1. **Launch the GUI** by running without arguments:

   ```bash
   python port_scanner.py
   ```

2. **Fill in the fields**:
   - **Target**: Enter IP address or hostname
   - **Start Port**: Beginning of port range
   - **End Port**: End of port range
   - **Timeout**: Connection timeout (seconds)
   - **Threads**: Number of concurrent workers

3. **Click "Start Scan"** to begin scanning

4. **View results** in the scrollable text area

#### GUI Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                     GUI WORKFLOW                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   1. INPUT PHASE                                             │
│      ┌─────────────────────────────────────┐                 │
│      │  Target:     [192.168.1.1_______]  │                 │
│      │  Start:      [1_________________]  │                 │
│      │  End:        [1000_______________] │                 │
│      │  Timeout:    [1.0________________] │                 │
│      │  Threads:    [100_______________]  │                 │
│      └─────────────────────────────────────┘                 │
│                        │                                     │
│                        ▼                                     │
│   2. SCAN PHASE (runs in background thread)                  │
│      ┌─────────────────────────────────────┐                 │
│      │  Scanning 192.168.1.1...          │                 │
│      │  [████████████░░░░░░░] 65%         │                 │
│      │  Ports scanned: 650/1000           │                 │
│      └─────────────────────────────────────┘                 │
│                        │                                     │
│                        ▼                                     │
│   3. RESULTS PHASE                                           │
│      ┌─────────────────────────────────────┐                 │
│      │  ✓ Port 22: SSH                     │                 │
│      │  ✓ Port 80: HTTP                    │                 │
│      │  ✓ Port 443: HTTPS                  │                 │
│      │                                      │                 │
│      │  Scan complete. 3 open ports found. │                 │
│      └─────────────────────────────────────┘                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Architecture

### Code Structure

```
port_scanner.py
│
├── COMMON_SERVICES (Dictionary)
│   └── Port-to-service name mappings
│
├── scan_port()
│   ├── Creates TCP socket
│   ├── Attempts connection (connect_ex)
│   └── Returns (port, service) if open
│
├── resolve_hostname()
│   ├── DNS resolution via socket.gethostbyname()
│   └── Raises ValueError on failure
│
├── run_gui()
│   ├── Tkinter window setup
│   ├── Input validation
│   └── Background scanning thread
│
└── main()
    ├── Argument parsing
    └── ThreadPoolExecutor orchestration
```

### Data Flow

```
User Input
    │
    ▼
┌─────────────────┐
│ Argument Parser  │  (CLI) or  │  Tkinter Widgets (GUI)
└────────┬────────┘            └────────────┬─────────┘
         │                              │
         │                              │
         ▼                              ▼
┌─────────────────────┐     ┌─────────────────────────┐
│ resolve_hostname()  │     │ Validation + Thread      │
│ (DNS Lookup)        │     │ Spawning                │
└────────┬────────────┘     └────────────┬────────────┘
         │                              │
         └──────────┬───────────────────┘
                    ▼
         ┌─────────────────────┐
         │ ThreadPoolExecutor   │
         │ (100 workers)       │
         └─────────┬───────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌─────────┐        ┌─────────┐
    │ Port 22 │        │ Port 80 │
    │ Check   │   ...  │ Check   │
    └────┬────┘        └────┬────┘
         │                   │
         └─────────┬─────────┘
                   ▼
         ┌─────────────────────┐
         │ Collect Results     │
         │ Sort & Display      │
         └─────────────────────┘
```

### Supported Services

| Port | Service | Description |
|------|---------|-------------|
| 21 | FTP | File Transfer Protocol |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Unencrypted text communications |
| 25 | SMTP | Email transmission |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Web traffic |
| 110 | POP3 | Email retrieval |
| 143 | IMAP | Email access protocol |
| 443 | HTTPS | Secure web traffic |
| 993 | IMAPS | Secure IMAP |
| 995 | POP3S | Secure POP3 |
| 3306 | MySQL | MySQL database |
| 3389 | RDP | Remote Desktop Protocol |
| 8080 | HTTP-Proxy | Alternative HTTP port |
| 8443 | HTTPS-Alt | Alternative HTTPS port |

---

## Ethical Use Policy

```
╔════════════════════════════════════════════════════════════════╗
║                      ⚠ IMPORTANT WARNING ⚠                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  This tool is provided for EDUCATIONAL PURPOSES ONLY.          ║
║                                                                ║
║  LAWFUL USE ONLY:                                             ║
║  ✓ Scan your own systems                                      ║
║  ✓ Scan systems you have explicit written permission to test  ║
║  ✓ Use in controlled lab environments                          ║
║  ✓ Learning about network security fundamentals                ║
║                                                                ║
║  PROHIBITED USE:                                              ║
║  ✗ Scanning systems without authorization                      ║
║  ✗ Attempting to exploit vulnerabilities                       ║
║  ✗ Any malicious or unauthorized activities                     ║
║  ✗ Bypassing security controls or access restrictions          ║
║                                                                ║
║  Unauthorized port scanning may be ILLEGAL in your jurisdiction ║
║  and can result in civil and/or criminal penalties.            ║
║                                                                ║
║  By using this tool, you accept full responsibility for your   ║
║  actions and any consequences that may arise.                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `Unable to resolve hostname` | DNS failure | Check internet connection; verify hostname spelling |
| `No open ports found` | Firewall blocking | Try different target; check if ports are actually open |
| `Connection refused` | Port closed/filtered | Normal behavior for closed ports |
| `Permission denied` | Low port numbers | Try ports > 1024; run with sudo (not recommended) |
| `GUI not responding` | Scan in progress | Wait for scan to complete; reduce thread count |
| `Timeout errors` | Network latency | Increase timeout value with `--timeout` |

### Performance Tips

```bash
# For faster scanning (local network)
python port_scanner.py 192.168.1.1 1 1024 --timeout 0.5 --threads 200

# For more reliable scanning (remote targets)
python port_scanner.py example.com 1 1000 --timeout 3.0 --threads 50
```

### Debugging

Enable verbose output by modifying the script:

```python
# Add to scan_port() for debugging
print(f"Scanning port {port}...")
```

---

## License

This project is provided for **educational purposes only**.

### Permissions
- ✓ Use for learning and research
- ✓ Modify and distribute (with attribution)
- ✓ Use in educational institutions

### Restrictions
- ✗ Use for malicious purposes
- ✗ Claim as your own work
- ✗ Use without attribution in commercial products

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## References

- [Python socket module documentation](https://docs.python.org/3/library/socket.html)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Nmap Port Scanning Basics](https://nmap.org/book/man-port-scanning-basics.html)

---

**Last Updated**: January 2026 
**Python Version**: 3.6+
