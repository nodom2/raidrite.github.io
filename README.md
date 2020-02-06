
##### Virtual Environment Configuration
If you are running PyCharm, you may need to configure the Python Interpreter for this project to use the virtual environment 
associated with this project.  Press `Ctrl+Alt+S` and select `Project: 4155` -> `Project Interpreter`.  Click the gear 
icon on the right and choose 'Add'.  In the dialog box that pops up, select `Virtualenv Environment` in the left pane
and then choose `Existing Environment`.  Click the `...` and navigate to this project directory, then into `venv/Scripts`
and choose `python.exe`.   That's it.
 
If your configuration is slightly different (or you're not using PyCharm) then you may need to run `source venv/bin/activate` 
to activate the virtual environment. 

##### Installing project packages
Once you have the virtual environment configured and active, you may need to run `pip` to update any packages associated 
with this project.  Open a console within your IDE and ensure that you're inside a virtual environment -- you should see `(venv)` 
to indicate that the virtual environment is active.  If not, you may need to run `source venv/bin/activate`.  If the 
`(venv)` is active, run `pip install -r requirements.txt` in the top level of this project folder.  This will ensure 
that all libraries are consistent throughout development. 

If you need to add a package while working on this project using `pip install somepackagename` be sure to run
`pip freeze > requirements.txt` to add this package to the project.  When you do this, you ensure that anyone else who
works on this project after your commit will be able to install the same package (and version) that you did.

##### Running Flask
In theory, spinning up the flask application should be as simple as typing `flask run` from the console.  However,
if this fails because FLASK_APP could not be found then you may need to run: (Windows) `set FLASK_APP=backend/backend.py` 
or (Mac) `export FLASK_APP=backend/backend.py`.  The `.flaskenv` in this project directory *should* handle this 
automatically (assuming all the packages in requirements.txt were installed with pip). 
