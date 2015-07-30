MILANO
------
Hacking Team Malware Detection Utility

https://www.rooksecurity.com

https://www.rooksecurity.com/hacking-team-malware-detection-utility/


DESCRIPTION
-----------
In order to ensure full transparency and growth to the Milano tool, we are releasing the source code on GitHub (link below). Our intentions are to give people a way to protect themselves. We want to make sure we are completely transparent with how our tool operates. In lieu of executing the binary, the .py script on GitHub can be leveraged.

This is the first time we have released tools to the public for free. We will continue to develop, improve, and grow our processes as these opportunities are identified. We truly appreciate the feedback and suggestions and will continue to take them into account with every release.


REQUIREMENTS
------------
    Python 2.7  - This should be installed by default for most *nix / OS X systems.
    py2exe      - This is only required if compiling into a Windows executable.


SETUP
-----
No setup is required when running the Python script (milano.py) from source.

The executable (milano.exe) that we have pre-built for convenience is already available in the win32 folder.

If building the Windows executable yourself is desired, py2exe is required. In the Milano source directory, run:

    python build_win32.py py2exe


EXECUTION
---------
Windows

    Run Milano (milano.exe, under the win32 folder) as administrator.
 
    Milano should be able to run under Windows 7+ without any extra effort.

    If running under Windows XP, you may need to obtain a copy of the Microsoft C runtime DLL on your system if it's not already present. This can be done by installing the Microsoft Visual C++ 2008 Redistributable Package (x86) from here: http://www.microsoft.com/en-us/download/details.aspx?id=29

    Alternatively, if you have Python 2.7 installed, you can run the command "python milano.py".

Linux/OS X

    Run the command "python milano.py" from the folder containing milano.py.


Copyright 2015 Rook Security, LLC. All rights reserved.
