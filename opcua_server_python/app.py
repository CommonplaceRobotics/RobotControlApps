"""
OPC UA Server Bridge for igus Robot Control
Connects to the robot gRPC interface and exposes robot state and control via OPC UA.

Usage:
    python app.py [grpc_target] [--opcua-port 4840] [--app-name OpcUaServer-Python]
"""

import argparse
import logging
import sys
import os
import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from OpcUaServer import OpcUaServer


def _configure_logging(level_name: str, log_file: str | None) -> None:
    """Set up root logger with a timestamped console handler and optional file handler."""
    level = getattr(logging, level_name.upper(), logging.INFO)

    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(fmt)
        handlers.append(file_handler)

    for h in handlers:
        h.setFormatter(fmt)

    logging.basicConfig(level=level, handlers=handlers, force=True)

    # Suppress overly verbose third-party loggers unless debug is requested.
    if level > logging.DEBUG:
        logging.getLogger("asyncua").setLevel(logging.WARNING)
        logging.getLogger("grpc").setLevel(logging.WARNING)


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
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Logging verbosity (default: INFO)')
    parser.add_argument('--log-file', default=None,
                        help='Optional path to write log output to a file')
    args = parser.parse_args()

    _configure_logging(args.log_level, args.log_file)
    log = logging.getLogger(__name__)

    log.info("Starting OPC UA Server Bridge")
    log.info("  gRPC target:      %s", args.grpc_target)
    log.info("  OPC UA port:      %s", args.opcua_port)
    log.info("  App name:         %s", args.app_name)
    log.info("  Update interval:  %ss", args.update_interval)
    log.info("  Log level:        %s", args.log_level)
    if args.log_file:
        log.info("  Log file:         %s", args.log_file)

    server = OpcUaServer(
        app_name=args.app_name,
        grpc_target=args.grpc_target,
        opcua_port=args.opcua_port,
        update_interval=args.update_interval,
    )

    def signal_handler(sig, frame):
        log.info("Shutdown requested (signal %s)", sig)
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server.run()  # blocks until stopped


if __name__ == '__main__':
    main()