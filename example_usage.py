import asyncio
from api_client import OVCirrusApiClient, Authenticator

# Configuration (replace with real values or load from .env)
API_BASE_URL = "https://eu.manage.ovcirrus.com/"
AUTH_URL = API_BASE_URL + "api/ov/v1/applications/authenticate"

EMAIL = "kahyean.yip@gmail.com"
PASSWORD = "Ciscotac%2688"
APP_ID = "671f13d3e0748137d6fc5a27"
APP_SECRET = "db0553664df3a0c7f86986619748096dab6d1b58a91f1be9dffd093e50426280"

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
    
    # Get current user profile
    current_profile_resp = await client.user.getUserProfile()
    if current_profile_resp:
        print("Name:" + " ".join([current_profile_resp.data.firstname,current_profile_resp.data.lastname]))
    else:
        print("Failed to get user profile")
    

    user_profile: UserProfile = current_profile_resp.data

    # Modify a field (e.g., change firstname)
    user_profile.firstname = "Samuel"

    # Call update method
    updated_resp = await client.user.updateUserProfile(user_profile)

    if updated_resp:
        print("Changed Name to:" + " ".join([updated_resp.data.firstname,updated_resp.data.lastname]))
    else:
        print("Update failed.")

    await client.close()

asyncio.run(main())
