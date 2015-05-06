'''
This module defines the TPAM SSHClient for interacting with the TPAM
SSH CLI.  Under the hood it uses paramiko to open an SSH connection and
execute commands on the remote server.  
'''

import re
import socket
import paramiko
import config
import error
from api_methods import api_2_5_11
from tpam.error import TPAMError

class SSHClient:
    """This class defines a TPAM SSHClient object, which leverages paramiko
    and provides functionality for performing TPAM commands via the SSH CLI
    """
    
    def __init__(self, **kwargs):
        """Initialize the TPAM SSH Client with a paramiko SSH Client"""
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Read client configuration from ~/.tccfg or <cwd>.tccfg
        cfg_opts = {}
        config.get_config(cfg_opts)

        # Override .tccfg settings with anything passed in as keyword args
        if "tpam_key" in kwargs:
            kwargs["tpam_key"] = config.expand_user_path(kwargs["tpam_key"])
        cfg_opts.update(kwargs)
        
        # Validate config and establish SSH connection
        try:
            config.validate(cfg_opts)
        except error.TPAMConfigError:
            raise
        else:
            try:
                self.conn.connect(cfg_opts["tpam_host"], 
                    username=cfg_opts["tpam_user"], 
                    key_filename=cfg_opts["tpam_key"]
                )
            except (paramiko.SSHException, socket.error) as se:
                raise error.TPAMConnectError(se)
        
        # Dynamically add API methods to class
        # TODO: API version? - should ask Dell to include a version API call
        for method_name in api_2_5_11:
            self._generate(method_name)
            
    
    def _generate(self, method_name):
        """Internal function to add API methods to class"""
        def genericExecFunc(**kwargs):
            cmd = self._prepare(method_name, kwargs)
            try:
                result = self._execute(cmd)
            except error.TPAMExecError:
                raise   # re-raise previous exception
            return self._eval_result(method_name, result)
        genericExecFunc.__name__ = method_name
        setattr(self, method_name, genericExecFunc)
    
    
    def disconnect(self):
        """ Close the paramiko ssh connection object """
        self.conn.close()


    def _execute(self, cmd):
        """Function executes the supplied command, performs some 
        checks and returns results
        """
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        out = stdout.readlines()
        err = stderr.readlines()
        if err:
            raise error.TPAMExecError(
                "\n".join(e.replace("\r\n", "") for e in err))
        else:
            return "\n".join(o.replace("\r\n","") for o in out)


    def _prepare(self, cmd, kwargs):
        """Clean up dictionary values for command execution"""
        # Build up the SSH command with the supplied options
        # Strip out/re-quote the dictionary values
        options = ""
        for k in kwargs:
            kwargs[k] = str(kwargs[k]).replace('"','')
            kwargs[k] = str(kwargs[k]).replace("'",'')
            kwargs[k] = str(kwargs[k]).replace('`','')
            options += '--%s "%s" ' % (k, kwargs[k])
        return '%s %s' % (cmd, options.strip())


    def _process_table(self, result):
        """Convert table-like output to list of dicts"""
        dictlist = []
        result = result.split("\n")
        keys = result[0].split("\t")
        for values in result[1:]:
            dictlist.append(dict(zip(keys,values.split("\t"))))
        return dictlist


    def _eval_result(self, method_name, result):
        """Evaluate output from TPAM SSH CLI command"""
        # There are a couple special cases to handle
        if method_name == "Retrieve":
            if ' ' in result:
                # Passwords can't have spaces, so this is an error string
                raise error.TPAMAPIError(result)
            else:
                return result
        if method_name == "AddPwdRequest":
            m = re.search("^RequestID:\s+(\d+-\d+).*Active/Approved", result)
            if m:
                return m.group(1)
            else:
                raise error.TPAMAPIError(result)        
        # Otherwise handle generic result processing
        else:
            if api_2_5_11[method_name][0] == "string":
                for successful_response in api_2_5_11[method_name][1]:
                    if successful_response in result.lower():
                        return result
                raise error.TPAMAPIError(result)
            elif api_2_5_11[method_name][0] == "table":
                if "Usage:" in result:
                    raise error.TPAMAPIError(result)
                else:
                    return self._process_table(result)
        

    def GetPassword(self, **kwargs):
        """ Convenience function for retrieving a password, not
        actually part of the TPAM API. Must be called with either 
        "ReasonText" (ISA) or "RequestNotes" (PPM Requestor) so the function
        can tell which method to use to retrieve the password
        """
        password = ""
        if "ReasonText" in kwargs:
            try:
                password = self.Retrieve(**kwargs)
            except error.TPAMError:
                raise
        elif "RequestNotes" in kwargs:
            try:
                requestID = self.AddPwdRequest(**kwargs)
            except error.TPAMError:
                raise
            else:
                try:
                    password = self.Retrieve(RequestID=requestID)
                except error.TPAMError:
                    raise
                finally:
                    cancel = kwargs["Cancel"] if "Cancel" in kwargs else "<empty>"
                    try:
                        self.Cancel(RequestID=requestID, Comment=cancel)
                    except error.TPAMError:
                        raise
        else:
            raise error.TPAMAPIError("ReasonText or RequestNotes required")
        return password
    
    
    def help(self, method=""):
        """Show list of API functions or get usage for a particular method"""
        if not method:
            for k, v in api_2_5_11.iteritems():
                print "%s (%s)," % (k, v[0]),
        else:
            stdin, stdout, stderr = self.conn.exec_command("{0} --help".format(method))
            print "\n".join(o.replace("\r\n","") for o in stdout.readlines())
