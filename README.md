# Project Grouper

<img src="./flaskapp/static/sample_screenshots/home_page.PNG" alt="Project Grouper Logo" width="400">

**Project Grouper** is a web application designed to connect students by allowing them to post and join projects. This platform facilitates collaboration among students with similar interests.

[View the Forked Repository](https://github.com/danieljbae/CSPB-3308-Group-Project)

## Setup & Usage

1. **Instantiate Virtual Environment**  
   *(Note: Use “python3 -m venv venv” if needed)*
   ```bash
   python -m venv venv
   ```

2. **Activate the Environment**  
   *(Note: Use “. venv/bin/activate” if needed)*
   ```bash
   source venv/Scripts/activate
   ```

3. **Install Dependencies**  
   *(Note: Use “pip3 install -r requirements.txt” if needed. For non-Windows users, comment out the `pywin32==300` requirement on line 55 of the `requirements.txt` file)*
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**  
   *(Note: For command prompt, replace `export` with `set`)*
   ```bash
   source load.sh
   ```

5. **Run the Application**
   ```bash
   flask run
   ```

Visit [localhost:5000](http://localhost:5000/) in your browser to view the project.

## Screenshots

- **Home Page**  
  <img src="./flaskapp/static/sample_screenshots/home_page.PNG" alt="Home Page" width="400">

- **Create Project**  
  <img src="./flaskapp/static/sample_screenshots/CreateProject.PNG" alt="Create Project" width="400">

- **Join Project**  
  <img src="./flaskapp/static/sample_screenshots/TeamMembers.PNG" alt="Join Project" width="400">
