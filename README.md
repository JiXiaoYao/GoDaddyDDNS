# GoDaddyDDNS
A DDNS Python script for GoDaddy

## How to use?

### First step:

Download *main.py* and *lang.json* and create a new call *"config.json"*

### Second step:

Edit *"config.json"* like following:

```json
{
    "name": "name",
    "domain": "domain",
    "key" : "key form GoDaddy",
    "secret" : "secret form GoDaddy"
}
```

The domain name will looks like this: name.domain

### Final step:

Open shell and cd into the directory which those files located in

Run this command:

```shell
python main.py
```
