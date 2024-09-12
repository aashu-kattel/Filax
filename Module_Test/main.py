import subprocess
import psutil
import speedtest
import socket
from scapy.all import traceroute
import sys
import time
import logging

def show_connected_devices():
    """
    Retrieve and display information about connected devices on the network.
    
    Returns:
    list: A list of strings, each representing a connected device with its IP, port, and hostname.
    """
    try:
        devices = []
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                try:
                    # Attempt to get the hostname of the connected device
                    hostname = socket.gethostbyaddr(conn.raddr.ip)[0]
                except socket.herror:
                    hostname = "Unknown"
                devices.append(f"IP: {conn.raddr.ip}, Port: {conn.raddr.port}, Hostname: {hostname}")
        return devices
    except psutil.AccessDenied:
        return ["Error: Access denied. Try running the script with administrator privileges."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

def get_internet_speed():
    """
    Measure and return the current internet speed (download, upload, and ping).
    
    Returns:
    str: A string containing download speed, upload speed, and ping.
    """
    try:
        st = speedtest.Speedtest()
        print("Testing download speed...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        print("Testing upload speed...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping
        return f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps, Ping: {ping:.2f} ms"
    except speedtest.SpeedtestException as e:
        return f"Speedtest error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def trace_route(destination):
    """
    Perform a traceroute to the specified destination.
    
    Args:
    destination (str): The IP address or hostname to trace.
    
    Returns:
    list: A list of strings representing each hop in the route.
    """
    try:
        result, _ = traceroute(destination, maxttl=30, timeout=2)
        route = []
        for sent, received in result:
            if received:
                route.append(f"{received.src} ({received.time*1000:.0f} ms)")
        return route if route else ["No route found"]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

def get_data_usage():
    """
    Retrieve the current network data usage.
    
    Returns:
    str: A string containing the total bytes sent and received.
    """
    try:
        net_io = psutil.net_io_counters()
        return f"Bytes sent: {net_io.bytes_sent:,}, Bytes received: {net_io.bytes_recv:,}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def print_menu():
    """Display the main menu options."""
    print("\nNetwork Utility Console App")
    print("1. Show Connected Devices")
    print("2. Current Internet Speed")
    print("3. Trace Route")
    print("4. Data Usage")
    print("5. Exit")

def get_user_choice():
    """
    Prompt the user for a menu choice and validate the input.
    
    Returns:
    int: The user's validated choice (1-5).
    """
    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to run the Network Utility Console App."""
    while True:
        print_menu()
        choice = get_user_choice()

        if choice == 1:
            devices = show_connected_devices()
            print("\nConnected Devices:")
            for device in devices:
                print(device)
        elif choice == 2:
            print("\nMeasuring internet speed...")
            speed = get_internet_speed()
            print(speed)
        elif choice == 3:
            destination = input("Enter the destination for traceroute: ")
            print(f"\nTracing route to {destination}...")
            route = trace_route(destination)
            for hop in route:
                print(hop)
        elif choice == 4:
            usage = get_data_usage()
            print("\nData Usage:")
            print(usage)
        elif choice == 5:
            print("Exiting...")
            sys.exit(0)
        
        # Pause before showing menu again to allow user to read the output
        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
        logging.getLogger('psutil').setLevel(logging.ERROR)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)