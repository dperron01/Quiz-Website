
This was our project for Web Based Info Systems.
This code is how we submitted it.
It is taken from our own school's version of gitlab.
Members:
Myself
Amandeep Singh
Arthur Pa
Hammad Hassan
HJ Singh

//////////////////////////////////////////////////

To deploy on vagrant run:  

> vagrant destroy   
> vagrant up

and access localhost:8080

If you are running in CSIL, you may have to comment-in these lines in Vagrantfile:
>chef.channel = "stable"  
>chef.version = "12.10.24"

**Test data and logins**  
Some test data is already within the system upon loading.  
The logins are:  

       (login_email     / password)
       
Admin:  admin@pquiz.com / 123456

User_1: ex1@pquiz.com   / 123456

User_2: ex2@pquiz.com   / 123456


**NOTE**  
As **Admin** user, you will need to approve topics and questions through the **Admin** tab in the navigation bar before they are available on the website.  
Also, please note that you should only approve questions whose topics have already been approved. 
(This would be the normal workflow for the application, but with supplied test data, an abnormal workflow could be achieved)

**List of features**  
-	Signup, login, sessions  
    o	Email verification upon signup  
    o	Password reset
-	Profile page  
    o	Update profile  
    o	Account deletion  
    o	Profile picture  
    o	Test history
-	User information  
    o	List of users
-	Navigation bar  
-	Content creation  
    o	Topic creation  
    o	Question creation for a specific topic
-	Quiz taking capabilities  
    o	Generate 5 random questions from database  
    o	Score generated at the end
-	Feedback  
    o	Rate topics  
    o	Comment on topics
-	Questions taken history  
-	Explore topics  
    o	by latest  
    o	by topic  
    o	by popularity (rating)
-	Search bar  
-	Admin functions  
    o	Separate account with different user power  
    o	Approve topics and questions submitted by users
-	Pagination  
    o	Variety of pages have a page list implemented
