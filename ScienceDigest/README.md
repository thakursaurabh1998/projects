# Science Digest

This is the first project of the Full Stack Nano Degree II by Udacity.

Version used for code is Python 2.7.

Steps to run this python script:

1. Clone this repository in any directory(or it can be downloaded in form of a zip file).
1. Run the Vagrant file and after the virtual machine has opened, run the command:
	> *cd /vagrant*
1. After this you have to run the *views.py* file. This is the main file which is created with Flask framework. Enter the command:
	> *python views.py*

	__*Before that we have to add client_secrets.json and fb_client_secrets.json files in this directory*__
1. After giving the command a server will be setup at *localhost:5000*
1. Open browser and put the address mentioned above, i.e. *localhost:5000*
1. You can login and then add, edit, delete your own articles.

*__The database file is also provided in the repo__*

## API endpoints can be accesed with the following links in JSON form

1. To get all the categories:
	> http://localhost:5000/digest.json
2. To get all the articles of given category:
	> http://localhost:5000/_category-name_/articles.json
3. To get a specific article:
	> http://localhost:5000/digest/_category-name_/_article-title_/article.json
	
## References

1. Made with Bootstrap.
1. SideNav learnt from w3schools.
1. Bootstrap navbar used.
1. Webapp is mobile friendly.
1. Google OAuth v2 is used for authentication and authorization purposes.