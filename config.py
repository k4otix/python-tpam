'''
Simple text file config; one key=value pair per line.

Global settings will be stored in the user's home directory in a hidden file.
Settings can also be stored in the directory of the calling script,
or explicitly passed to the TPAMClient constructor.  Global settings
will be overridden by directory settings, which will be overridden
by arguments passed to the constructor.

Example settings file:
----------------------
tpam_host=acme-tpamPrimary-1
tpam_user=tpam_admin
tpam_key=/absolute/path/to/clikey

This module also provides functions to create config files, via
set_global_config() and set_local_config()

'''

import os
import error
import utils

def parse_config(cfg, cfg_opts):
    """Parse a .tccfg file update cfg_opts dictionary"""
    with open(cfg, 'r') as myCfg:
        for line in myCfg:
            try:
                k, v = line.lower().split('=')
                cfg_opts.update({k.strip():v.strip()})
            except ValueError:
                pass
                # TODO - log config file syntax error


def get_config(cfg_opts):
    """Locate config files for TPAM SSH connection and set values"""   
    cfg_file = ".tccfg"
    cfg_files = [
        os.path.join(os.path.expanduser('~'), cfg_file),
        os.path.join(os.path.abspath(os.curdir), cfg_file)
    ]
    for f in cfg_files:
        try:
            parse_config(f, cfg_opts)
        except IOError:
            pass
    return cfg_opts
    

def validate(cfg_opts):
    """Validate config options, otherwise raise an exception"""
    
    # Check for presence and resolution of tpam_host
    if "tpam_host" in cfg_opts:
        if not utils.is_valid_host(cfg_opts["tpam_host"]):
            raise error.TPAMConfigError("Unable to resolve tpam_host %s" % cfg_opts["tpam_host"])
    else:
        raise error.TPAMConfigError("No value for 'tpam_host' has been specified")
    
    # Check for presence of tpam_user
    if not "tpam_user" in cfg_opts:
        raise error.TPAMConfigError("No value for 'tpam_user' has been specified")
    
    # Check for presence of tpam_key and existence of file
    if "tpam_key" in cfg_opts:
        if not os.path.isfile(cfg_opts["tpam_key"]):
            raise error.TPAMConfigError("tpam_key %s not found or cannot be read" % cfg_opts["tpam_key"])
    else:
        raise error.TPAMConfigError("No value for 'tpam_key' has been specified")
    

def set_local_config(**kwargs):
    """Generate a .tccfg file in the current directory"""
    _set_config(os.path.abspath(os.curdir), kwargs)


def set_global_config(**kwargs):
    """Generate a .tccfg file in the user's home directory"""
    _set_config(os.path.expanduser('~'), kwargs)

    
def _set_config(fpath, kwargs):
    """Helper function for set_local_config() and set_global_config()"""
    try:
        with open(os.path.join(fpath, ".tccfg"), "w") as f:
            if "tpam_host" in kwargs:
                f.write("%s=%s\n" % ("tpam_host", kwargs["tpam_host"]))
            if "tpam_user" in kwargs:
                f.write("%s=%s\n" % ("tpam_user", kwargs["tpam_user"]))
            if "tpam_key" in kwargs:
                kwargs["tpam_key"] = expand_user_path(kwargs["tpam_key"])
                f.write("%s=%s\n" % ("tpam_key", os.path.normpath(kwargs["tpam_key"])))
    except IOError as e:
        print("Could not write .tccfg file: %s" % e)


def expand_user_path(fpath):
    """Replace '~' in the path with absolute path if necessary"""
    return fpath.replace('~', os.path.expanduser('~'), 1) if fpath.startswith('~') else fpath
