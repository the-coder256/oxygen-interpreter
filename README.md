# Oxygen Intepreter v0.13
This program interprets Oxygen programs (.ox)

## How to Use
(assuming you are in the repo folder)
```
cd src
py main.py "<file_path>"
```

For example:
```
cd src
py main.py "../tests/test.ox"
```

You can also access the version (v0.7+):
```
py main.py --version
```

## Changelogs
v0.13:
- Added compound operators (+=, -=, *=, /=)
- Added increment (++) and decrement (--) operators

v0.12:
- Added while
- Added break and continue

v0.11:
- Added conditional operators (==, <, >, <=, >=)

v0.10:
- Added for loops

v0.9:
- Added else if
- Added new error messages

v0.8:
- Added arithmetic operators (+, -, *, /)

v0.7:
- Added function returning
- You can access the version of this interpreter via `py main.py --version`

v0.6:
- Added multi argument calls and multi parameter definitions
- Other small changes

v0.5:
- Added else

v0.4:
- Added function definitions
- Added scopes
- Other small changes

v0.3:
- Added if conditions
- Added more error messages

v0.2.1:
- Fixed some bugs
- Added some error messages

v0.2:
- Added variable assignment
- Improved function calling

v0.1:
- Release (you can print stuff)
