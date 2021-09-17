# Project Title: Group Project Finder

## Team members

- Alysha Pennypacker
- Bryson Murray
- Daniel Bae
- Garrett Lubin

## Setup for Git/Bash

1. clone repo
2. Instantiate virtual environment, then Activate venv
3. Install dependencies to venv
   > `git clone https://github.com/alyshapennypacker/CSPB-3308-Group-Project.git` > <br> `python -m venv venv` > <br> `source venv/Scripts/activate` > <br> `pip install -r requirements.txt`

## `Usage` for Git/Bash

Once project dependencies installed in venv

1. run shell script to activate venv and export enviroment variables
   > `source load.sh` > <br> for windows: change from `export` to `set`
2. Run command line command to init database and bootstrap with data
   > `flask bootstrap`
3. All test queries below can be run with
   > `python query_tables.py`

---

## Use case 1

Use case name:

- Initilaizing database with Stackoverflow survey data and sample data (bootstrap tables)

Description:

- Test that database is succesfully adding new entries

Pre-conditions

- Defined database structure (attributes and keys)

Test steps:

1. Run `query_tables.py` on tables with step 3 on `usage`
2. Then check outputs on test #1

Expected result:

- All sample entries found in `bootstrap_helper()` should be in their respective tables

Actual result:

- Tables contain all sample data

Status (Pass/Fail):

- Pass

Notes:

- N/A

Post-conditions:

- People can create projects and join created projects based off database values

---

## Use case 2

Use case name:

- Defining relationships with SQL-Alchemy `backref`

Description:

- Testing SQL-Alchemy's `backref`, a database table obj attribute to allow for easy bi-directional relationships.

Pre-conditions

- Database is loaded up with sample entries and relationship/foreign keys are hooked up between tables
- backrefs are defined

Test steps:

1. Run `query_tables.py` on tables with step 3 on `usage`
2. Then check outputs on test #2

Expected result:

- Child table entity can reference back to it's parent table using `backref` attribute name

Actual result:

- Child table entity can reference back to parent using dot notation (i.e. `some_skill.show_users()`, where show_users() is a backref to `Users` table from the skill variable)

Status (Pass/Fail):

- Pass

Notes:

- The string defined in `backref` will effectively create an invisible column in the table defined in so that relationships are bi-directional
- for example in our `Users` table we can set a backref to `Skills` table with `relationship(Skills, backref=<"show_users">)`

Post-conditions:

- People can create projects and join created projects based off database values

---

## Use case 3

Use case name:

- Many-to-many relationship and Junction table between `Projects` and `Users`

Description:

- Testing SQL-Alchemy's Junction tables in it's ability to self manage additions to junction table

Pre-conditions

- Database is loaded up with sample entries and relationship/foreign keys are hooked up between tables

Test steps:

1. Run `query_tables.py` on tables with step 3 on `usage`
2. Then check outputs on test #3 and #4

Expected result:

- When "members" (or `Users`) are added on `Projects` , our Junction table `user-project` will self-populate with these user-project pairs

Actual result:

- Junction table `user-project` contains all user-project pairs, without ever explicity adding any entries to the `user-project` table

Status (Pass/Fail):

- Pass

Notes:

- N/A

Post-conditions:

- We can now query the following:
  > - For a given project, find all its memebers (or users)
  > - For a given user, find all of their projects
