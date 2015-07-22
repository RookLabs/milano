Milano

Hacking Team Malware Detection Utility
https://www.rooksecurity.com/hacking-team-malware-detection-utility/


Description:

    In order to ensure full transparency and growth to the Milano tool we are releasing the source code on GitHub 
    (link below). Our intentions are to give people a way to protect themselves. The executable was created with 
    the lowest technical user in mind and now we want to make sure we are completely transparent with how our 
    tool operates. In lieu of executing the binary the .py script on GitHub can be leveraged. We have learned a 
    lot during our releases to include, removing '.DS_Store' from the zip, consistent folder/file names, etc.

    This is the first time we have released tools to the public for free. We will continue to develop, improve, 
    and grow our processes as these opportunities are identified. We truly appreciate the feedback and suggestions 
    and will continue to take them into account with every release.


Requirements:

    Python 2.7  - This should be installed by default for most *nix / OS X systems
    py2exe      - This is only required if compiling into a Windows executable


Setup:

    No setup is required when running the Python script (milano.py) from source.

    If a Windows executable is desired, py2exe is required. In the Milano source directory, run:

        python build_win32.py py2exe

    The executable (milano.exe) will be in the win32 folder after the build process completes.


Execution:

    Windows:

        Run milano.exe as administrator. This Windows executable can be obtained from Rook Security's downloads page, or compiled manually using py2exe. 

        Download locations:

            * Downloads page:         https://www.rooksecurity.com/resources/downloads/
            * Original MSI installer: https://www.rooksecurity.com/wp-content/uploads/2015/07/RookMilanoInstaller.zip
            * Original ZIP release:   https://www.rooksecurity.com/wp-content/uploads/2015/07/Package_1.zip

        Alternatively, run the command "python milano.py", if the Python 2.7 programming language is installed on this system.

    Linux/OS X:

        Run the command "python milano.py" from the folder containing milano.py.


Copyright 2015 Rook Security, LLC. All rights reserved.
