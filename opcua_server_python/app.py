"""
OPC UA Server Bridge for igus Robot Control
Connects to the robot gRPC interface and exposes robot state and control via OPC UA.

Usage:
    python app.py [--grpc-target localhost:50051] [--opcua-port 4840] [--app-name OpcUaServer-Python]
"""

import argparse
import sys
import os
import signal

# Allow importing shared modules from control_python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'control_python'))

from OpcUaServer import OpcUaServer


def main():
    parser = argparse.ArgumentParser(description='OPC UA Server Bridge for igus Robot Control')
    parser.add_argument('--grpc-target', default='localhost:50051',
                        help='gRPC target address (default: localhost:50051)')
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