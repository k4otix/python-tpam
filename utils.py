'''
This module defines miscellaneous functions to support the TPAM SSHClient
'''

import socket

def is_valid_host(hostname):
    """Resolve a hostname to see if it appears valid"""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False
