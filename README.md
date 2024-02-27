## Freesound Client

This Library is a wrapper around the freesound API, an application interface that allows you to browse, search and retrieve information stored in the Freesound.org Database. For more information visit the developer page

[https://freesound.org/help/developers/](https://freesound.org/help/developers/)

> **DISCLAIMER**
The official python library is the [freesound-python](https://github.com/MTG/freesound-python). This implementation has been developed for teaching purpose.

The [Freesound API](https://freesound.org/docs/api/index.html) is very well documented and it is a useful resource to make the best use out of this library.

### Before you start
#### Dependencies
This software depends on the `requests` library which can be installed globally or locally (in a virtual environment) via `pip`
```
pip install requests
```
or
```
pip3 install requests
```

#### The API Credentials
In order to use this software you need an account on [freesound.org](https://freesound.org) and apply for an API key following this link [https://freesound.org/apiv2/apply/](https://freesound.org/apiv2/apply/). The form is quite straight forward in the **Create new API credentials** you must give a **name** and a **description** to your *key*, accept the [terms of use ](https://freesound.org/help/tos_api/) and click on **Request new access crediantials**


#### Basic set up
create a new file and create two constants where you insert your [**API Credentials**](index.md#the-api-credentials):
```py
API_KEY=<your-api-key>
USER_ID=<your-user-id>
```
> **Note**: you can use an `.env` file to save your credentials in a safer place

then create an instance of the `FreeSoundClient` as follows

```py
from freesound import *

API_KEY=<your-api-key>
USER_ID=<your-user-id>

c = FreeSoundClient(USER_ID,API_KEY) # The API Client
```
Now you are ready to make requests to the **freesound.org Database**!

Please follow the [Tutorial](tutorial.md) or the [How To](how-to-guide.md) sections in the Documentation to learn how to get started with the **Freesound Client** Library

### Documentation

### Contributors
Davide Bardi
Francesca Seggioli
Alessandro Cagiano