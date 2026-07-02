import socket
import concurrent.futures
import argparse
import sys
import tkinter as tk
from tkinter import scrolledtext
import threading

# Common port-to-service mapping for well-known ports
# This is a subset; in a real scenario, you might use socket.getservbyport() or a more comprehensive database
COMMON_SERVICES = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    993: 'IMAPS',
    995: 'POP3S',
    3306: 'MySQL',
    3389: 'RDP',
    8080: 'HTTP-Proxy',
    8443: 'HTTPS-Alt'
}

def scan_port(target_ip, port, timeout=1):
    """
    Scans a single port on the target IP address.
    
    Args:
        target_ip (str): The IP address of the target.
        port (int): The port number to scan.
        timeout (float): Connection timeout in seconds.
    
    Returns:
        tuple: (port, service_name) if open, else None.
    
    This function attempts to establish a TCP connection to the specified port.
    If successful, it determines the service name using a common services dictionary
    or falls back to socket.getservbyport(). This is a basic service detection;
    advanced scanners might use banner grabbing or fingerprinting.
    """
    try:
        # Create a socket object for TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to avoid hanging on unresponsive ports
        sock.settimeout(timeout)
        # Attempt to connect to the target IP and port
        result = sock.connect_ex((target_ip, port))
        sock.close()
        
        if result == 0:
            # Port is open; determine service name
            service = COMMON_SERVICES.get(port, 'Unknown')
            if service == 'Unknown':
                try:
                    # Try to get service name from system (may not work for all ports)
                    service = socket.getservbyport(port)
                except OSError:
                    pass  # Keep as 'Unknown' if lookup fails
            return (port, service)
    except socket.timeout:
        # Handle connection timeout (port might be filtered or host unresponsive)
        pass
    except socket.error:
        # Handle other socket errors (e.g., network issues)
        pass
    return None

def resolve_hostname(hostname):
    """
    Resolves a hostname to an IP address.
    
    Args:
        hostname (str): The hostname to resolve.
    
    Returns:
        str: The resolved IP address.
    
    Raises:
        ValueError: If DNS resolution fails.
    
    DNS resolution is crucial for hostname inputs. If it fails, we raise an exception
    to handle it appropriately in the calling context.
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {e}")

def run_gui():
    """
    Launches the graphical user interface for the port scanner.
    
    This function creates a Tkinter window with input fields for scan parameters
    and a text area to display results. The scan runs in a separate thread to
    prevent the UI from freezing.
    """
    root = tk.Tk()
    root.title("Port Scanner - Educational Tool")
    
    # Input fields
    tk.Label(root, text="Target (IP or Hostname):").grid(row=0, column=0, sticky="e")
    target_entry = tk.Entry(root, width=30)
    target_entry.grid(row=0, column=1)
    
    tk.Label(root, text="Start Port:").grid(row=1, column=0, sticky="e")
    start_entry = tk.Entry(root, width=30)
    start_entry.grid(row=1, column=1)
    
    tk.Label(root, text="End Port:").grid(row=2, column=0, sticky="e")
    end_entry = tk.Entry(root, width=30)
    end_entry.grid(row=2, column=1)
    
    tk.Label(root, text="Timeout (seconds):").grid(row=3, column=0, sticky="e")
    timeout_entry = tk.Entry(root, width=30)
    timeout_entry.insert(0, "1.0")
    timeout_entry.grid(row=3, column=1)
    
    tk.Label(root, text="Threads:").grid(row=4, column=0, sticky="e")
    threads_entry = tk.Entry(root, width=30)
    threads_entry.insert(0, "100")
    threads_entry.grid(row=4, column=1)
    
    # Result display
    result_text = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
    result_text.grid(row=5, column=0, columnspan=2, pady=10)
    
    def start_scan():
        # Get input values
        target = target_entry.get().strip()
        try:
            start_port = int(start_entry.get())
            end_port = int(end_entry.get())
            timeout = float(timeout_entry.get())
            threads = int(threads_entry.get())
        except ValueError:
            result_text.insert(tk.END, "Error: Invalid input values. Please enter numbers for ports, timeout, and threads.\n")
            return
        
        # Validate inputs
        if not target:
            result_text.insert(tk.END, "Error: Target cannot be empty.\n")
            return
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            result_text.insert(tk.END, "Error: Invalid port range. Ports must be between 1 and 65535, and start <= end.\n")
            return
        if timeout <= 0 or threads < 1:
            result_text.insert(tk.END, "Error: Timeout must be positive, and threads must be at least 1.\n")
            return
        
        # Clear previous results
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Scanning {target} from port {start_port} to {end_port}...\n")
        scan_button.config(state="disabled")  # Disable button during scan
        
        def scan():
            try:
                target_ip = resolve_hostname(target)
                result_text.insert(tk.END, f"Resolved {target} to {target_ip}\n")
                ports = range(start_port, end_port + 1)
                open_ports = []
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = {executor.submit(scan_port, target_ip, port, timeout): port for port in ports}
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        if result:
                            open_ports.append(result)
                
                open_ports.sort()
                if open_ports:
                    result_text.insert(tk.END, "\nOpen ports found:\n")
                    for port, service in open_ports:
                        result_text.insert(tk.END, f"Port {port}: {service}\n")
                else:
                    result_text.insert(tk.END, "\nNo open ports found in the specified range.\n")
                
                result_text.insert(tk.END, f"\nScan complete. Total ports scanned: {len(ports)}\n")
            except ValueError as e:
                result_text.insert(tk.END, f"Error: {e}\n")
            except Exception as e:
                result_text.insert(tk.END, f"Unexpected error: {e}\n")
            finally:
                scan_button.config(state="normal")  # Re-enable button
        
        # Run scan in a separate thread to avoid blocking the UI
        threading.Thread(target=scan, daemon=True).start()
    
    # Scan button
    scan_button = tk.Button(root, text="Start Scan", command=start_scan, bg="lightblue")
    scan_button.grid(row=6, column=0, columnspan=2, pady=10)
    
    # Warning label
    warning_label = tk.Label(root, text="Use responsibly and only on systems you own or have permission to scan.", fg="red")
    warning_label.grid(row=7, column=0, columnspan=2)
    
    root.mainloop()

def main():
    """
    Main function to parse arguments and orchestrate the port scan.
    
    This function handles command-line argument parsing, hostname resolution,
    and multi-threaded port scanning using concurrent.futures.ThreadPoolExecutor.
    Multi-threading improves performance by scanning multiple ports concurrently,
    but be mindful of rate limiting and ethical use.
    """
    parser = argparse.ArgumentParser(description="Multi-threaded Open Port Scanner for Educational Purposes. "
                                                 "Use responsibly and only on systems you own or have permission to scan.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("start_port", type=int, help="Starting port number (inclusive)")
    parser.add_argument("end_port", type=int, help="Ending port number (inclusive)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads (default: 100)")
    
    args = parser.parse_args()
    
    # Validate port range
    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        raise ValueError("Invalid port range. Ports must be between 1 and 65535, and start_port <= end_port.")
    
    # Resolve hostname to IP if necessary
    target_ip = resolve_hostname(args.target)
    print(f"Scanning {args.target} ({target_ip}) from port {args.start_port} to {args.end_port}...")
    
    # Generate list of ports to scan
    ports = range(args.start_port, args.end_port + 1)
    
    # Use ThreadPoolExecutor for multi-threaded scanning
    # This allows concurrent execution, speeding up the scan
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit scan tasks for each port
        futures = {executor.submit(scan_port, target_ip, port, args.timeout): port for port in ports}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    
    # Sort and display results
    open_ports.sort()
    if open_ports:
        print("\nOpen ports found:")
        for port, service in open_ports:
            print(f"Port {port}: {service}")
    else:
        print("\nNo open ports found in the specified range.")
    
    print(f"\nScan complete. Total ports scanned: {len(ports)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run command-line interface
        try:
            main()
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Run graphical user interface
        run_gui()