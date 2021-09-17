''' Use this script to integrate and store the following data (on backend)
from stackoverflow survey 2020 data'''

# Intended to be General skill levels across languages, frameworks, topics
skill_level = {
    1: "Never heard of it",
    2: "Watched a few tutorials",
    3: "Have used in personal projects",
    4: "Have used in more advanced/complex projects",
    5: "Develop with professionally",
}


# https://insights.stackoverflow.com/survey/2020#developer-profile-developer-type-all-respondents
developerRolesTuple = [
    ('Developer, back-end', 55.2),
    ('Developer, full-stack', 54.9),
    ('Developer, front-end', 37.1),
    ('Developer, desktop or enterprise applications', 23.9),
    ('Developer, mobile', 19.2),
    ('DevOps specialist', 12.1),
    ('Database administrator', 11.6),
    ('Designer', 10.8),
    ('System administrator', 10.6),
    ('Developer, embedded applications or devices', 9.6),
    ('Data or business analyst', 8.2),
    ('Data scientist or machine learning specialist', 8.1),
    ('Developer, QA or test', 8.0),
    ('Engineer, data', 7.6),
    ('Academic researcher', 7.2),
    ('Educator', 5.9),
    ('Developer, game or graphics', 5.6),
    ('Engineering manager', 5.5),
    ('Product manager', 5.1),
    ('Scientist', 4.2),
    ('Engineer, site reliability', 3.9),
    ('Senior executive/VP', 2.7),
    ('Marketing or sales professional', 1.3),
]
roleNames = ['Developer, back-end', 'Developer, full-stack', 'Developer, front-end', 'Developer, desktop or enterprise applications', 'Developer, mobile',
             'DevOps specialist', 'Database administrator', 'Designer', 'System administrator', 'Developer, embedded applications or devices', 'Data or business analyst',
             'Data scientist or machine learning specialist', 'Developer, QA or test', 'Engineer, data', 'Academic researcher', 'Educator', 'Developer, game or graphics',
             'Engineering manager', 'Product manager', 'Scientist', 'Engineer, site reliability', 'Senior executive/VP', 'Marketing or sales professional']


# https://insights.stackoverflow.com/survey/2019#developer-roles
Industries = [
    ('Software development - other', 11.9),
    ('Information technology', 10.9),
    ('Financial and banking', 8.9),
    ('Software as a service (saas) development', 7.6),
    ('Web development or design', 7.6),
    ('Consulting', 7.0),
    ('Data and analytics', 5.7),
    ('Health care or social services', 4.4),
    ('Media, advertising, publishing, or entertainment', 3.9),
    ('Retail or ecommerce', 3.8),
    ('Internet', 3.3),
    ('Education and training', 3.3),
    ('Manufacturing', 2.8),
    ('Cloud-based solutions or services', 2.8),
    ('Government or public administration', 2.7),
    ('Research - academic or scientific', 2.6),
    ('Telecommunications', 2.3),
    ('Transportation', 2.0),
    ('Energy or utilities', 1.8),
    ('Security', 1.4),
    ('Marketing', 1.3),
    ('Travel', 1.1),
    ('Nonprofit', 0.6),
    ('Real estate', 0.6)
]
industryNames = ['Software development - other', 'Information technology', 'Financial and banking', 'Software as a service (saas) development', 'Web development or design', 'Consulting',
                 'Data and analytics', 'Health care or social services', 'Media, advertising, publishing, or entertainment', 'Retail or ecommerce',
                 'Internet', 'Education and training', 'Manufacturing', 'Cloud-based solutions or services', 'Government or public administration', 'Research - academic or scientific',
                 'Telecommunications', 'Transportation', 'Energy or utilities', 'Security', 'Marketing', 'Travel', 'Nonprofit', 'Real estate']


# https://insights.stackoverflow.com/survey/2019#technology
languages =[
    ("JavaScript", 67.8),
    ("HTML/CSS", 63.5),
    ("SQL", 54.4),
    ("Python",41.7),
    ("Java",41.1),
    ("Bash/Shell/PowerShell", 36.6),
    ("C#",31.0),
    ("PHP",26.4),
    ("C++",23.5),
    ("TypeScript",21.2),
    ("C",20.6),
    ("Ruby",8.4),
    ("Go",8.2),
    ("Assembly",6.7),
    ("Swift",6.6),
    ("Kotlin",6.4),
    ("R",5.8),
    ("VBA",5.5),
    ("Objective-C",4.8),
    ("Scala",3.8),
    ("Rust",3.2),
    ("Dart",1.9),
    ("Elixir",1.4),
    ("Clojure",1.4),
    ("WebAssembly",1.2)
]
languageNames = [
    'JavaScript', 'HTML/CSS', 'SQL', 'Python', 'Java', 'Bash/Shell/PowerShell', 'C#', 'PHP', 'C++', 
    'TypeScript', 'C', 'Ruby', 'Go', 'Assembly', 'Swift', 'Kotlin', 'R', 'VBA', 'Objective-C', 'Scala', 
    'Rust', 'Dart', 'Elixir', 'Clojure', 'WebAssembly']


# Table: ProjectInterests
# Correlated technologies graph
# Select up to 5 technologies you are profficient in
# Select up to 3 technologies you would like to learn

# https://insights.stackoverflow.com/survey/2020#correlated-technologies
