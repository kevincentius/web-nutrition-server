
Recommended setup guide (may be incomplete):

- IDE: [Eclipse (PyDev](http://www.eclipse.org/downloads/)
- Open Eclipse and choose a folder (workspace)
- Install PyDev:
	- In Eclipse: Help -> Install new software...
	- enter update site = http://www.pydev.org/updates
	- select PyDev, continue
	- (eclipse restart may be required)

- Setup git:
	- In Eclipse: Window -> Perspective -> Open perspective -> Others -> select Git
	- click inside the Git Repositories panel and paste https://github.com/kevincentius/web-nutrition-server.git and continue clone process
	- right click the new repository and import project (check the only project and finish)
	- go back to PyDev perspective (open perspective PyDev)
	- you can now pull by right click on project -> Team -> Pull
	- tip: Git Staging view is handy for committing local changes

- Run the project
	- right click server.py -> Run as... -> Python Run
	- server starts on port 8081
	- you can test analyze e.g. a wikipedia page by opening simply on browser: http://localhost:8081/nutrition?url=https://en.wikipedia.org/wiki/Chess (should see json response containing the analysis result)

