'''
This module implements an SSH wrapper for the Dell TPAM 2.5 SSH command line
interface.  Although not all functions have been fully tested, it works well
for the more common operations and implements a number of exceptions for error
checking.

This module can be used interactively from the Python interpreter or imported
into scripts as an easy way to interface with TPAM.

One caveat is that unlike the native SSH CLI, API methods and keyword arguments
are CASE SENSITIVE.  This may be fixed in a future enhancement but isn't that
important; the case matches what a user would see with the --help flags in the 
SSH CLI.

Each call to the API takes approx. 3 seconds to execute, which is certainly
less than ideal, especially when considering a user with a "Requestor" role
must make 3 calls to the API to retrieve a password.  Note that the third call
to the "Cancel" method isn't really required but significantly helps in cases
where another password retrieval may be made within the window of the previous
password release so that scripts/programs that are stateless can generate a 
new password request and not receive an error about there already being a
scheduled password release.

For the most part this module will just pass methods/arguments along to TPAM
and the appliance will determine if there is an error or not, but there are
cases where the module will interpret results and give a different response
back to the client.  There may be some cases where the module will interpret
results returned by TPAM to create a response for the client application that
is easier to consume.

'''

import tpam.client

