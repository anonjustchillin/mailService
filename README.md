# 2-Year Course Work
### Subject: Databases
### Topic: Testing software products
### Description
This application is a command line interface, or **CLI**, written in Python, using **Typer** (for convenient writing of the CLI application), **Rich** (for displaying tables, colored text in the console), **pyodbc** (for connecting to the SQL Server Management Studio database) libraries.
## Main commands
#### Functions available to everyone:
- log in and log out;

  ``python appcli.py login``

  ``python appcli.py logout``

- show all users of the product;

  ``python appcli.py show users``

- show all problems and suggestions;

  ``python appcli.py show problems``

- show the author of the course work.

  ``python appcli.py about``

#### Functions available to logged in users:
- show messages sent to the current user;
- show messages received by the current user;

  ``python appcli.py show messages``

- send a message;

  ``python appcli.py send``
  
- delete a message;

  ``python appcli.py delete message``

- show information about the current user.

  ``python appcli.py show myself``
  
#### Functions available to employees:
- add, update, delete a user;

  ``python appcli.py add user``
  
  ``python appcli.py update user``
  
  ``python appcli.py delete user``
  
- add, update, delete a problem or suggestion.

  ``python appcli.py add problem``
  
  ``python appcli.py update problem``
  
  ``python appcli.py delete problem``
  
