Granting Access to the Windows Server
1. Access Requirements:
To access the Windows Server, users must have an account under amer.pfizer.com or apac.pfizer.com.
2. Adding Users to Remote Desktop Users Group:
Open "lusrmgr.msc" (Local Users and Groups) on the Windows Server.

Navigate to "Groups" and then locate "Remote Desktop Users."

Click "Add" to add users to the group.

Click "Add" again and ensure that "Locations" is set to the specified location (amer.pfizer.com or apac.pfizer.com).

Enter the usernames you want to add, click "Check Names" to verify, and then click "OK."

Confirm by clicking "OK" to add the selected users to the "Remote Desktop Users" group.

Accessing the Windows Server
Once the users are added to the "Remote Desktop Users" group, they can access the Windows Server using Remote Desktop Connection:

Open "Remote Desktop Connection" on your local machine.

Enter the IP address or hostname of the Windows Server.

Use the credentials associated with the amer.pfizer.com or apac.pfizer.com accounts to log in.

You should now have remote access to the Windows Server.

By following these steps, you've successfully set up a Windows Server with the required software and granted access to users from specified Pfizer accounts. This configuration ensures a secure and efficient environment for development and other server-related tasks.
