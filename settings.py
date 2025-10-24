"""
This script provides a demonstration of various socket settings and error
handling scenarios as required by the project. It attempts to connect
to a target host to test socket timeout, buffer sizes (SO_RCVBUF, SO_SNDBUF),
and blocking vs. non-blocking connection modes.

It is designed to catch and log common network errors such as timeouts,
connection refused, and address resolution failures.
This module can be run standalone using command-line arguments or
imported by main.py.
"""

import argparse
import socket
import errno
import logging
import select
from pathlib import Path

def setup_logger(log_path: str | None):
    if not log_path:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
        return
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def print_and_log(msg: str, level="info"):
    print(msg)
    getattr(logging, level)(msg)

def apply_socket_settings(s: socket.socket, timeout: float, recvbuf: int, sendbuf: int, nonblocking: bool):
    s.settimeout(timeout)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recvbuf)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, sendbuf)
    s.setblocking(not nonblocking)

def connect_blocking(s: socket.socket, host: str, port: int):
    print_and_log(f"[Connect] (blocking) -> {host}:{port}")
    s.connect((host, port))

def connect_nonblocking(s: socket.socket, host: str, port: int, timeout: float):
    print_and_log(f"[Connect] (non-blocking) -> {host}:{port} with poll timeout={timeout}s")
    err = s.connect_ex((host, port))
    if err in (0, errno.EISCONN):
        return
    if err not in (errno.EINPROGRESS, errno.EWOULDBLOCK, errno.EALREADY):
        raise OSError(err, f"connect_ex failed: {errno.errorcode.get(err, err)}")
    
    r, w, x = select.select([], [s], [s], timeout)
    if s in w:
        e = s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if e != 0:
            raise OSError(e, f"SO_ERROR after select: {errno.errorcode.get(e, e)}")
        return
    raise TimeoutError(f"Non-blocking connect timed out after {timeout}s")

def demo_socket_settings(host: str, port: int, timeout: float, recvbuf: int, sendbuf: int, nonblocking: bool, log_path: str | None):
    setup_logger(log_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print_and_log("=== Socket Settings Demo ===")
        try:
            apply_socket_settings(s, timeout, recvbuf, sendbuf, nonblocking)

            applied = {
                "timeout": timeout,
                "blocking": s.getblocking(),
                "rcvbuf": s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF),
                "sndbuf": s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF),
                "family": "AF_INET",
                "type": "SOCK_STREAM",
            }
            print_and_log("[Settings] Applied:")
            for k, v in applied.items():
                print_and_log(f"  - {k}: {v}")

            if nonblocking:
                try:
                    connect_nonblocking(s, host, port, timeout)
                    print_and_log("[Connect] Success (non-blocking).")
                except TimeoutError as te:
                    print_and_log(f"[Error] {te}", "error")
                    return
            else:
                connect_blocking(s, host, port)
                print_and_log("[Connect] Success (blocking).")

            try:
                s.send(b"HEAD / HTTP/1.0\r\nHost: test\r\n\r\n")
                r, _, _ = select.select([s], [], [], 1.0)
                if r:
                    data = s.recv(1024)
                    print_and_log(f"[Recv] {len(data)} bytes received.")
                else:
                    print_and_log("[Recv] No data within 1s (this can be normal).")
            except (ConnectionResetError, BrokenPipeError) as e:
                print_and_log(f"[Warn] Data test failed: {e}", "warning")

        except socket.gaierror as e:
            print_and_log(f"[Error] Address resolution failed for {host}:{port} -> {e}", "error")
        except socket.timeout:
            print_and_log("[Error] Connection timed out.", "error")
        except ConnectionRefusedError:
            print_and_log("[Error] Connection refused (host reachable, port closed?).", "error")
        except OSError as e:
            print_and_log(f"[Error] OS error: [{e.errno}] {e.strerror}", "error")
        except Exception as e:
            print_and_log(f"[Error] Unexpected: {e}", "error")
        finally:
            print_and_log("=== Demo finished ===")

def main():
    ap = argparse.ArgumentParser(description="E. Error Management and Settings Module")
    ap.add_argument("--host", default="1.1.1.1", help="Target host/IP")
    ap.add_argument("--port", type=int, default=80, help="Target port")
    ap.add_argument("--timeout", type=float, default=2.0, help="Socket timeout (seconds)")
    ap.add_argument("--recvbuf", type=int, default=8192, help="SO_RCVBUF size (bytes)")
    ap.add_argument("--sendbuf", type=int, default=8192, help="SO_SNDBUF size (bytes)")
    ap.add_argument("--nonblocking", action="store_true", help="Use non-blocking connect")
    ap.add_argument("--log", help="Optional log file path (e.g., logs/settings.log)")
    args = ap.parse_args()

    demo_socket_settings(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        recvbuf=args.recvbuf,
        sendbuf=args.sendbuf,
        nonblocking=args.nonblocking,
        log_path=args.log,
    )

if __name__ == "__main__":
    main()