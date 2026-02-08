# Installation 

Can run this in a few ways, reccomended way would be to install it through pipx then run `pipx install .` when in the parent directory (the one with `pyproject.toml`). Note: if you are running an updated version, you will need to use `--force` to overwite the old scripts. Although a simple installation with `pip install .` does also work (but is quite a bit slower).

This then gives you two commands:
1. `foundrysetup` -> This opens a gui to setup some basic config to a json file. Note once this file is created you can manually edit it to add more levels or change the spacing on the levels, or even add more if you need. There is a convert button here also that lets you just run the second command through here.
2. `foundryconvert` -> This has a required input of a `.json` file for its config, it will then convert to the specified format given in the setup file.

Alternatively you can run both of them manually with uv or python, although you wil have to manage your directories a little more (and setup venvs etc).

# TODO:
- finalise the dd2vtt converter
- give more advanced options somewhere in another tab
- look into adding images to the files, current need to add them manually in foundry