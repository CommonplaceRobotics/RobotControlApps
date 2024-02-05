# App packaging
The app must packaged so that iRC / CPRog can upload it to the robot control. An app package is a zip file containing one or more app directories, which contain the app definition files, binaries and other app-dependent files.

## Packaging for execution on the robot control
Create a zip file of so that its structure is as follows. This way the robot control automatically starts your app.
```
.
└── <name of your app>
    ├── <main binary or python script>
    ├── rcapp.xml
    └── ui.xml
    └── <other files, directories, python scripts, etc. that the app depends on>
```

You can make your app cross-platform compatible by adding both the Raspberry Pi (no file extension) and Windows binaries (.exe). The robot control automatically chooses depending on the system.

## Packaging for remote execution
To run your app on a different device or for testing you need to remove the ```<executable.../>``` lines from ```rcapp.xml```. The app package only needs ```rcapp.xml``` and ```ui.xml``` in the same structure as above.

After installing and enabling the app in iRC / CPRog you can start and connect your app with the gRPC socket of the robot control. You can disconnect and restart at any time.

## Updating apps
The robot control provides an update installation mode that only changes the main files while keeping configuration.

Specifically it updates the following (if present):
* rcapp.xml
* ui.xml
* executables mentioned in rcapp.xml (but no other executables, libraries or scripts)
* AppData directory

If your app package contains apps that are not installed yet they will be installed normally.
