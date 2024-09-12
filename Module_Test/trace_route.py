import sys
import time
import logging

def traceroute(hostname):
    # Placeholder for the actual traceroute implementation
    print(f"Performing traceroute to {hostname}...")
    # Simulate traceroute output
    print("1  192.168.1.1  1.123 ms")
    print("2  10.0.0.1  2.456 ms")
    print("3  172.16.0.1  3.789 ms")
    print("4  8.8.8.8  4.012 ms")

def main():
    # Example hostname to test traceroute
    hostname = "google.com"
    traceroute(hostname)
    print("Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
        logging.getLogger('psutil').setLevel(logging.ERROR)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")