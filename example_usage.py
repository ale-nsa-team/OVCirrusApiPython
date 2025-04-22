import asyncio
from pprint import pprint
from api_client import OVCirrusApiClient, Authenticator

# Configuration (replace with real values or load from .env)
API_BASE_URL = "https://eu.manage.ovcirrus.com/"
AUTH_URL = API_BASE_URL + "api/ov/v1/applications/authenticate"

EMAIL = "kahyean.yip@gmail.com"
PASSWORD = "Ciscotac%2688"
APP_ID = "671f13d3e0748137d6fc5a27"
APP_SECRET = "db0553664df3a0c7f86986619748096dab6d1b58a91f1be9dffd093e50426280"

orgId = "632a9823803a31ad755226ee"
siteId = "633256c72f0723ac44277f3b"
deviceId = "6602790a979e77043c367e5d"
    
async def main():
    auth = (
        Authenticator()
        .setURL(AUTH_URL)
        .setCredentials(EMAIL, PASSWORD)
        .setApp(APP_ID, APP_SECRET)
        .build()
    )

    if(auth.get_token()):
        print("Authenticated successful!")

    client = OVCirrusApiClient(base_url=API_BASE_URL, auth=auth)
    
    # # Get current user profile
    # current_profile_resp = await client.user.getUserProfile()
    # if current_profile_resp:
    #     print("Name:" + " ".join([current_profile_resp.data.firstname,current_profile_resp.data.lastname]))
    # else:
    #     print("Failed to get user profile")
    
    # user_profile: UserProfile = current_profile_resp.data

    # # Modify a field (e.g., change firstname)
    # user_profile.firstname = "Samuel"

    # # Update name method
    # response = await client.user.updateUserProfile(user_profile)

    # if response:
    #     print("Changed Name to:" + " ".join([response.data.firstname,response.data.lastname]))
    # else:
    #     print("Update failed.")

    # # Get Organization method
    # response = await client.organization.getOrganization(orgId)
    # if response:
    #     print("Print Organization !")
    #     pprint(vars(response.data))
    # else:
    #     print("Failed.")

    # # Get Site method
    # response = await client.site.getSite(orgId, siteId)
    # if response:
    #     print("Print Site !")
    #     pprint(vars(response.data))
    # else:
    #     print("Failed.")        
            
    # # Get Device method
    # response = await client.device.getDevice(orgId, deviceId)
    # if response:
    #     print("Print device !")
    #     pprint(vars(response.data))
    # else:
    #     print("Failed.")      
    
    # await client.close()

    # Get current user profile
    device_resp = await client.device.getAllDevices("632a9823803a31ad755226ee","633256c72f0723ac44277f3b" )
    if device_resp:
        print("Print device !")
        pprint(vars(device_resp.data[0]))
    else:
        print("Failed.")    

    await client.close()        
    

asyncio.run(main())
