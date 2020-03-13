# 4155 Capstone Project
## Setup: For Pycharm
Open Pycharm.  If you have not cloned this repo, you can open it directly from Pycharm by clicking 'Get from Version Control' 
in the Welcome dialog box that pops up (assuming you have no other projects open).  Alternatively, you can clone this repo 
and create a pycharm project on that directory.  

## Switching `git` branches in Pycharm & Committing to Github
To switch to a different branch in Pycharm, look at the bottom-right corner of the IDE.  You should see `Git: master` 
(or some other branch name).  If you click that, you'll see a few choices for *remote* branches.  When you switch branches 
in Pycharm, it also switches what files you see in your OS (as far as I know).  So if you need to add a file to a branch, 
you can switch inside the IDE this way or use some command line utility to switch branches manually.  To commit changes 
to a branch in Pycharm, click the green check mark in the top right or click `VCS -> Commit` from the top menu.  After 
you commit changes, you still need to push them to github.  You can do this by hitting `ctrl/cmd + shift + k` or clicking 
`VCS -> Git -> Push` from the top menu.

### Setting up the Project Interpreter
Next, we have to tell Pycharm where to find whatever version of Python we'll be using.  Press `ctrl + alt + S` to open 
project settings (or click File -> Settings).   In the left pane of Settings, Click 'Project: 4155' (or whatever project 
name you may have specified -- should be below 'Version Control'.  Then click `Project Interpreter`.  In the right pane, 
click the gear icon next to the "Project Interpreter" field (at the top), then click `Add...`.  In the left pane of the 
new dialog box that pops up, click `Virtualenv Environment`.  In the right pane choose the `Existing Environment` radio 
button, and click the `...` icon next to the `Interpreter` field.  In the file browser that pops up, navigate to the 
current project directory (from the github repo that you cloned or opened, this should be called `4155`); within that 
directory navigate to `venv\Scripts\python.exe`.  Click `Ok` several times to get back to the IDE.  

##### If this doesn't work for you....
If setting up the project interpreter as described doesn't work for you then you will need to create a new virtual environment
(outside the working directory of this project) and then install the libraries for this project using `pip` with 
`requirements.txt` *while the new virtual environment is active*.  If you created a new virtual environment
for this project, click `Terminal` at the very bottom of Pycharm.  *Make sure that you are working on the intended branch* 
(`twitch-client` in this case), and then run `pip install -f requirements.txt`.  

This should install all the libraries you need to run any python files in this project to the virtual environment where
you ran `pip install`.

### Other step
There are two other things you'll need to do before you can run anything.  You'll need to download `settings.py` from the 
shared google drive folder (in the `Code-Related` folder).  Before copying, make sure the branch you want to copy it to
is *active* (`twitch-client` in this case).  Copy `settings.py` to the `app/` folder of this project.  This file contains
the secret key from twitch (which is why it's not included in this repo). 

### Verifying Success
After copying `settings.py` to the `app/` folder, you can check whether you're good to go by running one of the unit tests.  
Navigate to `app\tests\` in the `Project` tab in the left pane of Pycharm and double click to open one of the unit test 
files.  You should see a green play button next to the `class Test...` definition.  Click it to run tests.