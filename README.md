# python-tpam
Python wrapper for Dell's TPAM command line API

Users of Dell's Total Privileged Access Manager (TPAM) can select from several languages to interact with the product programatically, including Perl, Java, C++ and shell.  I prefer to work in Python, so I wrote a module that can easily be imprted into Python scripts or used in an interactive Python shell.  Underneath is a Paramiko SSH client sending commands to the appliance.

This README file includes some basic usage; there is further documentation embedded in the comments of the .py files themselves.

DISCLAIMER: I am not a software development nor a Python expert so I'm sure there are probably better to ways to implement what I've done here; but it has been more than sufficient for my use cases and I have not yet come across any bugs in my day-to-day use of the module.  It was written and tested against Python 2.7.

Usage
=====
TPAM Config File (.tccfg)
--------------------------
The TPAM module supports a hierarchical configuration specification in which settings passed to the client's constructor have the highest precedence, followed by a .tccfg file in the working directory, and finally a .tccfg file in the user's home directory.  This file specifies the appliance host name, the TPAM user name, and an absolute path to the user's API key/SSH cert.

Example:
```INI
tpam_host=acme-tpam-1
tpam_user=admin
tpam_key=/path/to/admin/key
```

Additionally, the client.py file contains methods to create a local (working directory) or global (user's home directory) file for you:
```python
>>> from tpam import config
>>> config.set_local_config(tpam_host="acme-tpam-1", tpam_user="admin", tpam_key="/path/to/admin/key")  # OR
>>> config.set_global_config(tpam_host="acme-tpam-1", tpam_user="admin", tpam_key="/path/to/admin/key")
```
Example: Retrieve a list of all TPAM systems with "sql" in the host name
---------
```python
>>> import tpam
>>> tc = tpam.client.SSHClient()   # Settings being read from a .tccfg file
>>> >>> tc.help()
AddAccount (string), AddCollectionMember (string), AddCollection (string), AddGroupMember (string), AddGroup (string), AddPwdRequest (string), AddSystem (string), AddSyncPass (string), AddSyncPwdSub (string), AddUser (string), Approve (string), Cancel (string), ChangeUserPassword (string), CheckPassword (string), DeleteAccount (string), DeleteSyncPass (string), DeleteSystem (string), DeleteUser (string), DropCollectionMember (string), DropCollection (string), DropGroupMember (string), DropGroup (string), DropSyncPwdSub (string), ForceReset (string), GetPwdRequest (table), ListAccounts (table), ListAcctsForPwdRequest (table), ListAssignedPolicies (table), ListCollectionMembership (table), ListCollections (table), ListDependentSystems (table), ListGroupMembership (table), ListGroups (table), ListRequestDetails (table), ListReasonCodes (table), ListRequest (table), ListSystems (table), ListSynchronizedPasswords (table), ListSyncPwdSubscribers (table), ListUsers (table), ReportActivity (table), Retrieve (string), SetAccessPolicy (string), SSHKey (string), SyncPassForceReset (string), TestSystem (string), UnlockUser (string), UpdateAccount (string), UpdateDependentSystems (string), UpdateSyncPass (string), UpdateSystem (string), UpdateUser (string), UserSSHKey (string),
>>> tc.help("ListSystems")

Usage: ListSystems --System sysname [options...]

Options may be specified in any order.  Option values which accept more than
one word, i.e., --Description, must surround the value with double quotes
Option Names are not case sensitive and may be abbreviated to uniqueness

                  Req/                                                         
Option Name       Opt  Description                                             
================= ==== ========================================================
--SystemName      Opt  System Name to filter.  Use * for wildcard.
--NetworkAddress  Opt  Network Address to filter.  Use * for wildcard.
--CollectionName  Opt  Collection Name for membership to filter.  Use * for
                       wildcard.
--Platform        Opt  Name of specific platform to filter or All (default).
                       See the documentation for a list of supported values.
                       Use "Custom/customPlatName" for a custom platform.
--AutoFlag        Opt  Y/N or All for all systems regardless of automation.
--SortOrder       Opt  One of SystemName (default), NetworkAddress,
                       PlatformName.
--MaxRows         Opt  Maximum number of rows to return.  Default=25
--Help            Opt  Print this help message and exit                        

Legacy Support only for the following values:
ListSystems [SystemName (* for wildcard)],[ParentName (obsolete - ignored)],
[NetworkAddress (* for wildcard)],[CollectionName (* for wildcard)],
[Platform (All| (see Supported platform list)) default=All],
[SysAutoFl (All|Y|N) default=All],
[Sort (SystemName|NetworkAddress|PlatformName) default=SystemName],
[MaxRows Default=25]
>>> sql_servers = tc.ListSystems(SystemName="*sql*", MaxRows=0)
>>> len(sql_servers)
3
>>> for s in sql_servers:
...     print s["NetworkAddress"], s["PlatformName"]
... 
10.5.2.23 Linux
10.5.2.24 Linux
10.31.8.3 Windows
>>> tc.disconnect()
```
