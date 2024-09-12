import streamlit as st
import subprocess
import psutil
import speedtest
import socket
from scapy.all import traceroute
import sys
import time
import logging

def show_connected_devices():
    try:
        devices = []
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                try:
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
    try:
        st.write("Testing internet speed...")
        speed_test = speedtest.Speedtest()
        download_speed = speed_test.download() / 1_000_000
        upload_speed = speed_test.upload() / 1_000_000
        ping = speed_test.results.ping
        return f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps, Ping: {ping:.2f} ms"
    except speedtest.SpeedtestException as e:
        return f"Speedtest error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def trace_route(destination):
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
    try:
        net_io = psutil.net_io_counters()
        return f"Bytes sent: {net_io.bytes_sent:,}, Bytes received: {net_io.bytes_recv:,}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.set_page_config(page_title="Network Utility App", page_icon="🌐")
    st.title("Network Utility Application")

    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Select an option:", 
                              ["Show Connected Devices", 
                               "Current Internet Speed", 
                               "Trace Route", 
                               "Data Usage"])

    if choice == "Show Connected Devices":
        st.header("Connected Devices")
        devices = show_connected_devices()
        for device in devices:
            st.text(device)

    elif choice == "Current Internet Speed":
        st.header("Internet Speed Test")
        if st.button("Run Speed Test"):
            with st.spinner("Testing internet speed..."):
                speed = get_internet_speed()
            st.success(speed)

    elif choice == "Trace Route":
        st.header("Trace Route")
        destination = st.text_input("Enter the destination for traceroute:")
        if st.button("Trace"):
            with st.spinner(f"Tracing route to {destination}..."):
                route = trace_route(destination)
            for hop in route:
                st.text(hop)

    elif choice == "Data Usage":
        st.header("Data Usage")
        usage = get_data_usage()
        st.text(usage)

if __name__ == "__main__":
    logging.getLogger('psutil').setLevel(logging.ERROR)
    main()