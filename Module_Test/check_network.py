import psutil

def check_network_counters():
    try:
        net_io = psutil.net_io_counters()
        print(f"Bytes Sent: {net_io.bytes_sent}")
        print(f"Bytes Received: {net_io.bytes_recv}")
        print(f"Packets Sent: {net_io.packets_sent}")
        print(f"Packets Received: {net_io.packets_recv}")
    except Exception as e:
        print(f"An error occurred: {e}")

check_network_counters()