'''
This module defines exceptions for the TPAM SSHClient.
All exceptions inherit from TPAMError for convenience so the
client code has the option to catch specific errors or a more generic
TPAMError.

'''

class TPAMError(Exception):
    """Base error class for TPAM module errors"""
    pass
        

class TPAMConfigError(TPAMError):
    """Exception for a fatal client configuration error"""
    def __init__(self, message):
        TPAMError.__init__(self, message)
        

class TPAMConnectError(TPAMError):
    """Exception for a fatal client connection error"""
    def __init__(self, message):
        TPAMError.__init__(self, message)
        

class TPAMExecError(TPAMError):
    """Exception for a SSH client execution error"""
    def __init__(self, message):
        TPAMError.__init__(self, message)


class TPAMAPIError(TPAMError):
    """Exception for a TPAM API result error (ex - system not found)"""
    def __init__(self, message):
        TPAMError.__init__(self, message)
