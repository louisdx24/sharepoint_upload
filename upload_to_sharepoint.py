#credit to https://yzhums.com/60151/
#pre-requisites: 
# 1. registered an app in azure develop
# 2. configure Microsoft Graph permission, in my case, Sites.ReadWrite.All.
# More information regarding permission could be found here https://yzhums.com/60151/

import requests

def get_access_token(tenant_id, client_id, client_secret):
        access_token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        data = {"client_id": client_id,
                "scope": "https://graph.microsoft.com/.default",
                "client_secret": client_secret,
                "grant_type": "client_credentials"}
        response = requests.post(access_token_url, data = data)
        access_token = response.json()["access_token"]
        return access_token

def get_drive_id(site_id, access_token):
        #site_id could be obtained via adding "_api/site/id" at the end of the your sharepoint site URL
        drive_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        headers = {
                "Authorization": f'Bearer {access_token}'
                }
        response = requests.get(drive_url, headers=headers)
        drive_value = response.json()["value"]
        value = drive_value[0]
        drive_id = value["id"]
        return drive_id

def update_to_qc_sharepoint(folderpath, file_name, data): 
        #data parameter is included when file is from other source, for unloading an existing file, no need for data parameter
        #folderpath information: path of the folder inside the sharepoint, replace space with "%20"
        #When uploading an existing file, file_name should be the same as the file to be uploaded

        client_id = "" #client id of Azure app
        client_secret = "" #the value of client secret, not secret id
        tenant = "" #tenant id of Azure app
        site_id = "" #sharepoint site id could be obtained via adding "_api/site/id" at the end of the your sharepoint site URL
        access_token = get_access_token(tenant, client_id, client_secret)
        drive_id = get_drive_id(site_id, access_token)

        upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folderpath}/{file_name}:/content"
        upload_headers = {"Authorization": f'Bearer {access_token}',
           "Content-Type": "text/csv"}

        response = requests.put(upload_url, headers = upload_headers, data = data)
        return response.json()
