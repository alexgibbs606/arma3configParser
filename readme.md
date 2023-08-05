Used to parse ARMA 3 config dumps into more useful formats. This package doesn't require external packages, so it's as simple as:
```shell
python3 configParser.py AiO.1.92.145639_CUP.cpp
```

In the backend, the config data is loaded into a python dictionary, more documentation on how the config file parser works is to come.

For those who don't want to parse the file or use Python, a json file is provided that can be easily parsed in your language of choice or a json viewer; however, the file is very large, so I would recommend against a json viewer.