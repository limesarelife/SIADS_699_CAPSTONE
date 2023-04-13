# SIADS_699_CAPSTONE
 TEAM ANIMAL CROSSING
 
 ![alt text](https://github.com/limesarelife/SIADS_699_CAPSTONE/blob/main/BANNER-TEST-AC.png)
   # What ACNH Villager Are You App

Animal Crossing New Horizon (ACNH) is a Nintendo game that features user creativity by developing an island where villagers can come to visit and live as neighbors. The game allows players to create and customize their own island paradise by building infrastructure, landscaping, and decorating with furniture and other items. Players take on the role of a human avatar, who moves to the island, where they meet various animal villagers who also take up residence on the island overtime. These villagers have unique personalities and interests, and players can interact with them by engaging in conversations, completing tasks, and giving them gifts.In addition to designing and managing the island, players can also go fishing, catch bugs, and collect materials to craft items.

There are 391 villagers in the ACNH universe, each with unique personalities and characteristics. The villagers are categorized into different species such as dog, cat, deer, bird and more. Each species has its own set of characteristics, such as preferred hobbies, catchphrases, and clothing styles. And each villager has their own personality, ranging from snooty and smug to peppy and lazy. One island can have up to 10 depending on what other Switch player profiles are already on the island and how much available land there is on the island to build villager homes.  Most players average between 5 to 8 villagers per island.

The determination of a user's villager most “like” them happens via a website quiz which involves utilizing unique villager personalities and traits of each of the 391 villagers in Animal Crossing: New Horizons (ACNH).  An information retrieval system was built which takes into account the characteristics of each villager and matches them with the user's preferences and personality traits. For example, if a user indicates that they are lazy and into music, the system might match them with a villager who is also lazy and enjoys listening to music.  If there is a tie between multiple villagers that are matched with the user's personality, the system utilizes villager overall popularity values to break ties. Villager overall popularity values are determined by the Google Trends and ACP Polls total values combined for a villager.  Overall, this quiz provides a fun and interactive way for users to engage with the ACNH universe and connect with a villager that they can relate to on a personal level. 

## Objective

Our ultimate objective for our capstone project was to develop a full-stack web app that includes an information retrieval with ranking for breaking ties that is capable of suggesting Animal Crossing Villager that best matches the user's preferences, based on the options selected in the drop-down quiz and similarity rating. Our Minimum Viable Product (MVP), consists of utilizing several Python libraries, including Pandas, Numpy, and Sklearn for implementing cosine similarity and using Django for front end-to-back end web development; connecting the website with the information retrieval systems to ingest and utilize the user's quiz responses. For web design, we used HTML and CSS, and created an Animal Crossing New Horizons aesthetic. From the frontend to backend we are storing the user responses to the second quiz (after the villager options are presented to the user) in a Postgres database table in order to see which information retrieval system is preferred. In order to manage DNS and hosting, we utilized various AWS products/services such as AWS Route 53 for DNS, and deployment via AWS Elastic Beanstalk which provides and spins up EC2 instances and load balancers in order to run our app which connects to a AWS Postgres RDS to store the second quiz responses.  We really enjoy the platform as a service model for small projects such as our given that AWS Elastic Beanstalk handles and scales easily. Ultimately our goal was to apply the skills we learned in our Cloud Computing, Recommender Systems and Machine Learning Pipelines classes to achieve our objective of a fully deployed, end-to-end web application, inclusive of the information retrieval system, on AWS.

## Framework

Built with:
- Django
- AWS Elastic Beanstalk & AWS RDS (Postgres)

## Features:

- Two Information Retrieval Systems
- Villager Analysis
- Local set up with Postgres via pgadmin
- Production setup with AWS Elastic Beanstalk
- Works on Safari, Google Chrome, Mozilla and Microsoft Edge browsers

## Installation

This project was built using python - Django. For setting up, firstly ensure you have python downloaded and installed, at least 3.7 or newer.  Then proceed to install Django in your command prompt.
    pip install django
To read about Django go to the documentation here:
https://docs.djangoproject.com/en/4.2/

### Clone the Repository

To clone the repo, run these lines of code in your terminal:

You will want to change directory into the DEV_699 branch, that is where the Django application and its project folder and all requirements reside. 

    git clone https://github.com/limesarelife/SIADS_699_CAPSTONE.git

    cd DEV_699

Why a separate branch? Well, we will be adding, overtime, more applications to this project as a way to stay connected after our capstone project so this is not the final version of this or the main branch - we also love playing ACNH.  Message us for our island codes or to be Switch friends 😀

### Virtual environment

Before installing the packages required for this app/project you will need to create a virtual environment. Create virtual environment and name it, we are calling ours venv:

    python3 -m venv venv

Next, activate the virtual environment by running the following command (this is for Unix/macOS):

    source venv/bin/activate

To deactivate the virtual environment just type deactivate into the terminal.

**Note:** You should exclude your virtual environment directory from your version control system using .gitignore or similar.  To read more information about virtual environments go here:
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

Once that is done, install the packages and dependencies used in this application/project within the requirements.txt file. You do not need to pip freeze at this point because we have listed all needed packages/dependencies for you that are needed to create and run this application.  To do this, run the following commands:

    pip install -r requirements.txt


## How to use - Run on Local Server

**Note:** In the settings.py file for ALLOWED_HOSTS in the list add on your local host to run this locally. Never set or leave the Allowed Hosts as ‘*’ - this is dangerous and bad practice.

Example: 

    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

Also, for best practices when running in a non-production environment you can switch DEBUG = False to DEBUG = True if you wish to do so.

Download and install pgadmin.  For macOS it's best to do so via HomeBrew and follow the instructions in the articles below.  You will want to create a user for your pgadmin as well a database and then login credentials for your user. 

These two articles provide great instructions on how to install:
Basic Homebrew Postgresql instructions:
https://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/

This article explains how to install as well as create a new database and create a new user and alter the role and set a password:
https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/

You will want to save all your environment variables to your machine inorder to utilize os.environ.get() when connecting to your Postgres database, never save or commit information to a public repository as it can introduce malicious attacks on your application/project. 

Variables you will want to save locally will be ‘DJANGO_DB_NAME’, ‘DJANGO_DB_HOST’, ‘DJANGO_DB_PORT’, ’DJANGO_DB_USER’, ‘DJANGO_DB_PASSWORD’for your connection to your database.  While saving your environment variable to your machine make sure to also create and save an environment variable named ‘DJANGO_SECRET_KEY’ this should be a random string of anything that is longer than 50 random characters.


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DJANGO_DB_NAME'),
            'HOST': os.environ.get('DJANGO_DB_HOST'),
            'PORT': os.environ.get('DJANGO_DB_PORT'),
            'USER': os.environ.get("DJANGO_DB_USER"),
            'PASSWORD': os.environ.get("DJANGO_DB_PASSWORD"),
        }
    }


Django can easily use operating system environment variables to connect via the settings.py file to your Postgres database, to read more about Django Settings go here: 
https://docs.djangoproject.com/en/4.2/topics/settings/

We have already added all needed details for Postgres to properly interact with the application/project in the requirements.txt and in the settings.py and models.py so no need to change anything.

Once pgadmin is set up in your code editor, run the application by typing python manage.py runserver in your terminal to make sure everything is working as should and there are no other configuration or settings changes to be made and all the dependencies are installed.  If everything is okay the next step is to migrate our user response data from the second quiz to the database.  To do this run the following code:

    python manage.py makemigrations
    python manage.py migrate 
    python manage.py createsuperuser
    python manage.py runserver

*Now you're running locally, congrats!*

## How to use - Run/Host with AWS Elastic Beanstalk

To get started with AWS Elastic Beanstalk, you will need to create an AWS account here. After creating your AWS account and an IAMuser role account with programmatic access (you will want the key and secret), make sure that your virtual environment, venv, is activated and install the AWS EB CLI in it. After installation, verify that it has been installed correctly.

    pip install awsebcli

We have already created the django.config file for this application/project so no need to change anything (initialization of the RDS as well as the config for the WGSI).  

**Note:** There will be various permissions settings that will need to be applied to the various roles within your platforms application and IAMUser Role, these can easily be changed in the AWS console. Examples would be  AmazonEC2FullAccess, AWSElasticeBeanstalkFullAccess,and PowerUserAccess.

**Make sure that you are in DEV_699.**  Next run, eb init, this will initialize Elastic Beanstalk which will generate questions below:

1. Application Name (select default)
2. It appears that you are using Python (select Y)
3. Default Region (select us-east-1)
4. User Credentials (these are the credentials for your IAM user role credentials) and only will be asked for once.
5. Platform and Platform Branch (select Python 3.8 running on 64bit Amazon Linux 2)
6. CodeCommit (select No we are using GitHub 🙂)
7. SSH (select Y)
8. Key Pair (you will want to go with default and it will generate one for you but you can create a Key Pair once set up and use the named pair moving forward if you so choose, you can do this by going to the AWS Elastic Beanstalk console and in the EC2 instance and create an RSA key pair and note for use in this step.)

After completing the eb init questionnaire above a hidden directory named ".elasticbeanstalk" will be created in your editor . The directory should contain a config.yml file, with all the data you've just provided.

Next create the Elastic Beanstalk environment by running the following in your terminal. This also is followed by a few prompts to answer.

    eb create

1. Environment Name (select default, this refers to the name of your EB environment)
2. DNS CNAME Prefix (select default for now, this prefix is the one to be used when setting up your domain name)
3. Load balancer (select default which should be option 2 and type: Application)
4. Spot Fleet Requests (select No)

This will take a few minutes at least so grab a snack and wait. We are basically waiting on AWS to create and launch all our various resources needed such as EC2 instances, load balancers, security settings/permissions and auto scaling groups.
Go into your settings.py file and in the ALLOWED_HOSTS add the DNS CNAME to the list of allowed hosts. 

To deploy this application, run the deploy command:

    eb deploy

Now, there will be errors but by typing eb console it will open up the console on AWS, we will need to go to the EB instance running that we just created and go to the configurations and scroll all the way down and go to database, select edit and set up our default RDS along with the username and password (remember these).  Note that AWS handles all these environment variables for you so no need to add them as environment variables and as mentioned previously we already have added these to the .ebextension and django.config file for you.  You will want the following set up and then hit apply this will take a minute to update the environment:

    Engine: postgres
    Engine version: (select default populated)
    Instance class: db.t3.micro
    Storage: 10 GB (using default 5GB will cause error)
    Username: pick a username
    Password: pick a strong password

Next step in the same configuration area after the database is set up and applied to the environment go ahead and go to software and scroll all the way down.  In the environment variables add the DJANGO_SECRET_KEY and the string value hit apply/save.

As mentioned a few times after the environment update is done, Elastic Beanstalk will automatically pass the following database credentials and secret key to our Django app via the settings.py as variables.  We did all the settings.py for you and configurations in the yml file for making migrations and container commands.

Now, git add . and git commit all the various changes we have made. Elastic Beanstalk always uses the last commit we did so it’s important that as changes and configurations are made we commit to GitHub. Lastly!!!
    eb deploy
    eb open

*And your up and running 🎉*

## Villager Analysis:
Generate data used for application and used in the villager analysis downstream. 
Order of run for data creation: 
1. villagers_acnh.py: Combines all ACP Poll data per villager. pytrends_script.py: Utilizes each villager name and pulls historical number of searches on Google via PyTrends and related queries (searches) - DO NOT RUN unless you fetch cookies and place them in a gitignore and curl into the network.
2. villagers_final_connect.py: Combines the resultant csv files from the villagers_acnh.py and pytrends_script.py
3. villager_features.py: adds needed features for the villagers in order to create the user questionnaire for the 4. information retrieval and similarity measure. For example, astrology signs and music genres are added in this script, resultant file is the villager_final.csv which is used in the Django application/project

Utilized ACP Polls and Google Trends via PyTrends in order to find overall popularity of a villager.

Fetch initial ACNH data to understand overall villager popularity 
1. PyTrends to gather Google searches for ACNH villager popularity.
2. Animal Crossing Player poll results to compare with PyTrends results

Villager analysis with visuals found in the python_scripts_villagers folder and within the villager_analysis_w_viz.ipynb file.
1. Visual Package 1 - Stacked bar Charts Species & Personality compared to Species and Astrological Sign
2. Visual Package 2 - Bubble/Scatter Chart Google vs ACNH Poll results compared by Species and Personality
3. Visual Package 3 - Stacked Bar Chart Overall Popularity By Personality and Astrology

Information retrieval system that returns the villager most “like” a user via Villager 
Option 1 (from LSI) and Villager Option 2 (from Word Embeddings).  Results are pulled from Postgres database table and exported then saved in the python_scripts_villagers folder and read into the villager_analysis_w_viz.ipynb
1. User Information Retrieval System LSI vs Word Embeddings visual


## Attribution:

https://docs.djangoproject.com/en/4.2/
https://docs.djangoproject.com/en/4.2/topics/settings/
https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/
https://www.pgadmin.org/
https://pypi.org/project/awsebcli/3.7.4/
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html#command-options-general-elasticbeanstalkapplicationenvironment

To add your own purchased domain name follow these steps:

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-beanstalk-environment.html#routing-to-beanstalk-environment-create-alias-procedure
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html

Villager Analysis:

https://www.animalcrossingportal.com/tier-lists/new-horizons/all-villagers/
https://github.com/GeneralMills/pytrends
https://scikit-learn.org/stable/
https://spacy.io/usage/embeddings-transformers
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl
https://pandas.pydata.org/
https://numpy.org/
https://seaborn.pydata.org/
https://matplotlib.org/
https://plotly.com/python/plotly-express/

All the JSON data from this API is under CC BY 4.0 license, the images and music assets are the sole property of Nintendo.
https://github.com/alexislours/ACNHAPI/tree/master/images/villagers



 ![alt text](https://github.com/limesarelife/SIADS_699_CAPSTONE/blob/main/IMG_3436.JPG)
