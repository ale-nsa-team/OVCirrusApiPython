
# OmniVista Cirrus API Library for Python - **OVCirrusApi**

**OVCirrusApi** is a lightweight python library that enables developers to interact seamlessly with the OmniVista Cirrus RESTful API.

---

## ✨ Supported APIs

The full API documentation is available at: [OmniVista Cirrus API Docs](https://eu.manage.ovcirrus.com/apidoc/apidoc.html)

- Authentication API
- User API
- Device API
- Organization API
- Site API

---

## 🛠️ Built With

- **python 3.8**
    dependencies = [
        "httpx>=0.24.1",
        "requests>=2.31.0",
        "pydantic>=2.0",
        "pybreaker>=0.7.0",
        "backoff>=2.2.1"
    ]

---

## 🚀 Installation


To install manually:

1. Download the `ovcirrusapi-x.x.x.aar` file and place it in the `libs/` folder of your project.
2. Add the following to your `build.gradle.kts`:
   ```kotlin
   implementation(files("libs/ovcirrusapi-x.x.x.aar"))
   ```
3. Sync your Gradle files.

---

## 📦 Usage Guide

### Step 1: Create a global instance


In your `MainActivity` or `Application` class:

```python
    # auth_instance.py
    from api_client.auth import Authenticator
    auth = (
        Authenticator()
        .setURL("https://api.example.com/auth")
        .setCredentials("your@email.com", "your_password")
        .setApp("your_app_id", "your_app_secret")
        .build()
    )
```

### Step 2: Import the instance and 

```python

    from auth_instance import auth
    
    client = AsyncAPIClient(base_url=API_BASE_URL, auth=auth)
    userProfile = await client.getUserProfile()
    if userProfile is None:
        print("Failed to retrieve profile.")
        return

    print(userProfile.firstname)

```
## 🧪 Try the Demo App

1. Clone the repository to your local device.
2. Open the project using Android Studio.
3. Build and run the app on a physical device.
4. Generate a **Text QR Code** with the following format:
   ```json
   {
       "email": "<your_email>",
       "password": "<your_password>",
       "appId": "<your_app_id>",
       "appSecret": "<your_app_secret>",
       "apiBaseUrl": "<your_api_base_url>"
   }
   ```
5. Scan the QR code with your device's camera.
6. Tap the **Login** button to authenticate.

   View the demo [here](https://www.youtube.com/shorts/Fq7wqiczGAw)


---

## 📚 Available Methods

| Method                        | Description                                      | Documentation Link                                                                                                                                      |
|------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `authenticate`               | Authenticates and retrieves a token              | [Authentication API](https://docs.ovcirrus.com/ov/authentication-api)                                                                                   |
| `getUserProfile`             | Retrieves the user profile                       | [User Profile - GET](https://eu.manage.ovcirrus.com/apidoc/apidoc.html#tag/User/paths/~1ov~1v1~1user~1profile/get)                                      |
| `updateUserProfile`          | Updates the user profile                         | [User Profile - PUT](https://eu.manage.ovcirrus.com/apidoc/apidoc.html#tag/User/paths/~1ov~1v1~1user~1profile/put)                                      |
| `createADevice`              | Creates a device under a site                    | [Create Device](https://eu.manage.ovcirrus.com/apidoc/apidoc.html#tag/Device/paths/~1ov~1v1~1organizations~1%7BorgId%7D~1sites~1%7BsiteId%7D~1devices/post) |
| `getAllDevices`              | Gets all devices within a specific site          | [Site Devices](https://eu.manage.ovcirrus.com/apidoc/apidoc.html#tag/Device/paths/~1ov~1v1~1organizations~1%7BorgId%7D~1sites~1%7BsiteId%7D~1devices/get) |
| `getAllDevicesFromOrganization` | Retrieves all devices across an organization   | [Organization Devices](https://eu.manage.ovcirrus.com/apidoc/apidoc.html#tag/Device/paths/~1ov~1v1~1organizations~1%7BorgId%7D~1sites~1devices/get)        |

---
Test

## 📦 Releases

| Version          | Date       | Notes           |
|------------------|------------|-----------------|
| v10.4.3 Build 03 | 2025-04-16 | Initial release |

Visit the [Releases](https://github.com/Samuelyip74/OVCirrusApiBuilder/releases/tag/10.4.3) page to download `.zip` packages.

---

## 📄 License

```
Copyright (c) Samuel Yip Kah Yean 2025

This software is licensed for personal, non-commercial use only.

You are NOT permitted to:
- Use this software for any commercial purposes.
- Modify, adapt, reverse-engineer, or create derivative works.
- Distribute, sublicense, or share this software.

All rights are reserved by the author.

For commercial licensing or permission inquiries, please contact:
kahyean.yip@gmail.com
```


