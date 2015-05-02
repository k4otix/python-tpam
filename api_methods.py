'''
This module defines the list of TPAM API methods.  The dictionary keys are
the method names which are dynamically added to the client.SSHClient() object,
and the values are lists where:
v[0] = type<str> [string|table] to indicate what the API method returns, and
v[1] = type<list> [type<str>, ...] to indicate a list of strings that the API
       method returns upon successful completion (or an existing successful condition)
       
Note that v[1] is not necessary for API methods that return a table.
'''

from collections import OrderedDict

api_2_5_11 = OrderedDict()
api_2_5_11['AddAccount']                  = ["string", ["saved successfully"]]
api_2_5_11['AddCollectionMember']         = ["string", ["saved successfully"]]
api_2_5_11['AddCollection']               = ["string", ["created successfully"]]
api_2_5_11['AddGroupMember']              = ["string", ["saved successfully"]]
api_2_5_11['AddGroup']                    = ["string", ["created successfully"]]
api_2_5_11['AddPwdRequest']               = ["string", ["active/approved"]]
api_2_5_11['AddSystem']                   = ["string", ["saved successfully"]]
api_2_5_11['AddSyncPass']                 = ["string", ["created successfully"]]
api_2_5_11['AddSyncPwdSub']               = ["string", ["added successfully", "already subscribed"]]
api_2_5_11['AddUser']                     = ["string", ["added successfully"]]
api_2_5_11['Approve']                     = ["string", ["submitted successfully"]]
api_2_5_11['Cancel']                      = ["string", ["submitted successfully"]]
api_2_5_11['ChangeUserPassword']          = ["string", ["successfully changed"]]
api_2_5_11['CheckPassword']               = ["string", ["processed the password check"]]
api_2_5_11['DeleteAccount']               = ["string", ["successfully deleted"]]
api_2_5_11['DeleteSyncPass']              = ["string", ["successfully deleted"]]
api_2_5_11['DeleteSystem']                = ["string", ["successfully deleted"]]
api_2_5_11['DeleteUser']                  = ["string", ["successfully deleted"]]
api_2_5_11['DropCollectionMember']        = ["string", ["saved successfully"]]
api_2_5_11['DropCollection']              = ["string", ["successfully deleted"]]
api_2_5_11['DropGroupMember']             = ["string", ["saved successfully"]]
api_2_5_11['DropGroup']                   = ["string", ["successfully deleted"]]
api_2_5_11['DropSyncPwdSub']              = ["string", ["removed successfully"]]
api_2_5_11['ForceReset']                  = ["string", ["processed the password change"]]
api_2_5_11['GetPwdRequest']               = ["table", []]
api_2_5_11['ListAccounts']                = ["table", []]
api_2_5_11['ListAcctsForPwdRequest']      = ["table", []]
api_2_5_11['ListAssignedPolicies']        = ["table", []]
api_2_5_11['ListCollectionMembership']    = ["table", []]
api_2_5_11['ListCollections']             = ["table", []]
api_2_5_11['ListDependentSystems']        = ["table", []]
api_2_5_11['ListGroupMembership']         = ["table", []]
api_2_5_11['ListGroups']                  = ["table", []]
api_2_5_11['ListRequestDetails']          = ["table", []] # NOT TESTED
api_2_5_11['ListReasonCodes']             = ["table", []] # NOT TESTED
api_2_5_11['ListRequest']                 = ["table", []]
api_2_5_11['ListSystems']                 = ["table", []]
api_2_5_11['ListSynchronizedPasswords']   = ["table", []]
api_2_5_11['ListSyncPwdSubscribers']      = ["table", []]
api_2_5_11['ListUsers']                   = ["table", []]
api_2_5_11['ReportActivity']              = ["table", []]
api_2_5_11['Retrieve']                    = ["string", []]
api_2_5_11['SetAccessPolicy']             = ["string", ["successfully!"]]
api_2_5_11['SSHKey']                      = ["string", ["private key"]] # NOT TESTED
api_2_5_11['SyncPassForceReset']          = ["string", ["successfully scheduled"]]
api_2_5_11['TestSystem']                  = ["string", ["was successful"]]
api_2_5_11['UnlockUser']                  = ["string", ["unlocked successfully", "not currently locked"]]
api_2_5_11['UpdateAccount']               = ["string", ["saved successfully"]]
api_2_5_11['UpdateDependentSystems']      = ["string", ["saved successfully"]] # NOT TESTED
api_2_5_11['UpdateSyncPass']              = ["string", ["updated successfully"]]
api_2_5_11['UpdateSystem']                = ["string", ["saved successfully"]]
api_2_5_11['UpdateUser']                  = ["string", ["updated successfully"]]
api_2_5_11['UserSSHKey']                  = ["string", ["private key"]]
