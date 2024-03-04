## Freesound Client

This Library is a wrapper around the freesound API, an application interface that allows you to browse, search and retrieve information stored in the Freesound.org Database. For more information visit the developer page

[https://freesound.org/help/developers/](https://freesound.org/help/developers/)

> **DISCLAIMER**
The official python library is the [freesound-python](https://github.com/MTG/freesound-python). This implementation has been developed for teaching purpose.

The [Freesound API](https://freesound.org/docs/api/index.html) is very well documented, and it is a useful resource to make the best use out of this library.

#### Python Versions
This project has different branches for the following Python versions:

- main (3.11)
- 3.10
- 3.8

for full annotation and hints support download and use `main`

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


## Documentation
You can find tutorials and the full documentation of this library at the following link: [https://ddgg-el.github.io/freesound-client/](https://ddgg-el.github.io/freesound-client/)


### A special thanks to
Davide Bardi

Francesca Seggioli

Alessandro Cagiano

Marco Rotondella

for their collaboration in developing this library