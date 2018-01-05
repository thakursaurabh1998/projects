# Logs Analysis
This is the third project of the Full Stack Nano Degree by Udacity.

Version used for code is Python 2.7.

Steps to run this python script:

1. Clone this repository in any directory(or it can be downloaded in form of a zip file).
1. Run the Vagrant file and after the virtual machine has opened, run the command:
	> *cd /vagrant*
1. After this you have to run the *dbF.py* file. Enter the command:
	> *python dbF.py*
1. After the program has run successfully, three text files will be created presenting its output in clearly formatted plain text.

* Problem Statement 1 - article_views.txt
* Problem Statement 2 - authors_views.txt
* Problem Statement 3 - errors.txt

*__These text files are also provided in the repo.__*

## View Definitions

1. __Total Requests in a single day__
    > create view total as 
    > select count(*) as total,date(time) 
    > from log 
	> group by date(time) 
    > order by date(time);
1. __Total Errors in a single day__
	> create view errors as
	> select count(*) as errors,date(time)
	> from log
	> where status like '4%'
	> group by date(time)
	> order by date(time);
1. __Percentage of errors in a single day__
	> create view percentage as
    > select (cast(errors.errors as float)/cast(total.total as float))*100
    > as percentage,total.date
    > from errors natural join total;