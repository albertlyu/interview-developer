# mlb-angular

## Overview
This project was built with AngularJS, a JavaScript framework maintained by Google.

![Screenshot1](/images/screenshot1.png)
![Screenshot2](/images/screenshot2.png)

## Instructions
Install this project's dependencies with the Bower package manager. If you do not have Bower installed, install it globally by executing ```sudo npm install -g bower```, then within the mlb-angular folder, run the following command:
```
bower install
```
This installs mlb-angular's dependencies, including AngularJS 1.3, Twitter Bootstrap 3.3, and so on. Now start a simple Python server with one of the following commands depending on your version of Python:
```
python -m SimpleHTTPServer # Python 2
python3 -m http.server # Or Python 3
```
To view the application, open ```localhost:8000``` in your favorite web browser.

## Discussion
* AngularJS
* Bower
* Bootstrap Modals
* angular-local-storage for HTML5 web storage

## To Do
- [x] Load roster.json via controller
- [x] Convert inches to feet, date of birth to age
- [x] Add mug shots, including default mugshot for C.J. Edwards
- [x] Add orderBy filter on expression predicate
- [x] Add search bar
- [x] Create modal to save and view player notes
- [x] Manage dependencies with Bower
- [x] Persist notes data using [angular-local-storage](https://github.com/grevory/angular-local-storage)
- [x] Add Wrigley Field as background image
- [x] Add screenshot of application