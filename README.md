# Project Grouper

Project Grouper is webapp to connect students by posting/joining projects, with other students that have similar interests.
- [Linked to forked Repo](https://github.com/danieljbae/CSPB-3308-Group-Project)

***



### Set up and Usage

1. Instantiate Virtual Environment (alternatively you may need to use “python3 -m venv venv”)
> ```python -m venv venv ```

2. Activate Environment (alternatively you may need to use “. venv/bin/activate”)
> ``` source venv/Scripts/activate ``` 

3. Install dependencies (alternatively you may need to use  “pip3 install -r requirements.txt”)
> ```pip install -r requirements.txt```  
>- Please note if you are not using Windows to # comment out the pywin32==300 requirement on line 55 of the `requirements.txt` file

4. Set environment variables by running the following shell script (if you’re using command prompt replace ```export``` with ```set```)
> ```source load.sh``` <br>
     
5. Use command-line commands (once environment variables have been set) 
> ```flask run``` 

You should now be able to view this project on your local machine's browser at Port 5000  `<localhost>:5000`
***

### Example Screenshots

#### Home Page
![Home Page](./flaskapp/static/sample_screenshots/home_page.PNG)

#### Create Project
![Create Project](./flaskapp/static/sample_screenshots/CreateProject.PNG)

#### Join Project
![Join Project](./flaskapp/static/sample_screenshots/TeamMembers.PNG)
