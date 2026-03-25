"""
OPC UA Server Bridge for igus Robot Control
Connects to the robot gRPC interface and exposes robot state and control via OPC UA.

Usage:
    python app.py [grpc_target] [--opcua-port 4840] [--app-name OpcUaServer-Python]
"""

import argparse
import sys
import os
import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from OpcUaServer import OpcUaServer


def main():
    parser = argparse.ArgumentParser(description='OPC UA Server Bridge for igus Robot Control')
    # Positional argument: the robot control passes the connection target as argv[1] on startup.
    parser.add_argument('grpc_target', nargs='?', default='localhost:5000',
                        help='gRPC target address (default: localhost:5000)')
    parser.add_argument('--opcua-port', type=int, default=4840,
                        help='OPC UA server port (default: 4840)')
    parser.add_argument('--app-name', default='OpcUaServer-Python',
                        help='App name as registered in rcapp.xml (default: OpcUaServer-Python)')
    parser.add_argument('--update-interval', type=float, default=0.2,
                        help='Robot state polling interval in seconds (default: 0.2)')
    args = parser.parse_args()

    print(f"Starting OPC UA Server Bridge")
    print(f"  gRPC target:      {args.grpc_target}")
    print(f"  OPC UA port:      {args.opcua_port}")
    print(f"  App name:         {args.app_name}")
    print(f"  Update interval:  {args.update_interval}s")

    server = OpcUaServer(
        app_name=args.app_name,
        grpc_target=args.grpc_target,
        opcua_port=args.opcua_port,
        update_interval=args.update_interval,
    )

    def signal_handler(sig, frame):
        print("\nShutting down...")
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server.run()  # blocks until stopped


if __name__ == '__main__':
    main()