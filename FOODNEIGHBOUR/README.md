# CSC2033_Group16_Project - FoodShare Application
## [Link to GitHub Repository](https://github.com/newcastleuniversity-computing/CSC2033_Group16_Project)

## Overview
This project is part of our **CSC2033 (Software Engineering)** module, where we were tasked with creating a project that addresses at least one of the 17 UN Sustainability Goals. Our focus was on the second goal: achieving **zero hunger**.

To contribute to this goal, we developed a system designed to reduce food waste and support the local community. Our platform is intuitive to use, easy to operate, and packed with functionality. Key features include:

- **User Account System**: Users can create an account, log in, and manage their profiles.
- **Ad Interaction**: Users can view and interact with ads posted by others. This includes commenting, bookmarking, and reporting ads.
- **Ad Feed**: Users have a homepage displaying nearby ads which they can customise to their preference using a variety of location and time based filters/sort-methods.
- **Social Features**: Users can view and friend other user profiles.
- **Ad Management**: Users can create, view, and delete their own ads.
- **Settings Page**: Users can modify their details through a settings page.
- **Admin Panel**: Admin users have the capability to perform CRUD operations (Create, Read, Update, Delete) on user accounts.

Our goal was to build a robust platform that not only helps reduce food waste but also fosters community engagement. For
more details or information about the project feel free to read more of our documentation including contribution matrix, test cases and GUI showcase available **[[HERE]](https://drive.google.com/drive/folders/15O2TDPTsKWFNmDfzp0SaDLAYDDbu0zBR?usp=sharing) (also available In project submission).**

---
## Usage
Any important information concerning the usage and running of the program:

- **Python 3.10.x Required**: [Download Python](https://www.python.org/downloads/release/python-31014/)
- **PyCharm 2024.1 Recommended** [Download PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)
- **Git Required**: [Download Git](https://git-scm.com/downloads)
- Install Dependencies Required: `pip install -r requirements.txt`
- **Database URL & Details**: `mysql://sql8698080:rFpjPWykZa@sql8.freesqldatabase.com/sql8698080`
- **Admin Login Information**: Email: Admin@gmail.com Password: Admin
- **Run: `python Main.py`**

---
## Coding Standards
Due to the nature of the project with multiple developers working on it its important to maintain a standardized coding
style, here is a basic run down of said style:
- **Class Names & Package/File Names**: We chose to display these all in the UpperCamelCase (Pascal) convention.
- **Database Table Names**: Similarly we chose to display these in Pascal case to align with the mapped classes.
- **Variable Names**: We chose to display these in snake_case convention.
- **Database Column Names**: snake_case to align with variable names.
- **File Structure**: The Folder is broken down into backend, frontend, images and tests with further subdirectories in
each.
- **Code Line Length**: Code line length adheres to PyCharms recommended line length.
- **Error Handling**: Error handling is only used when needed to increase maintain a degree of performance.
---
## Acknowledgements
A brief section of acknowledgments associated with the project includes:

### Contributors
People who contributed to the project:
- Dan Dingley
- Ishan Kalra
- Ain Fatihah
- Maria Papadopoulou
- Azam Butt
- Drew Wandless

### Libraries
Libraries used in the project, as specified in `requirements.txt`:
- **[mysqlclient](https://pypi.org/project/mysqlclient/)**: A Python interface to MySQL, used for connecting to and interacting with the MySQL database.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: A SQL toolkit and Object-Relational Mapping (ORM) library for Python, providing a full suite of well-known enterprise-level persistence patterns.
- **[captcha](https://pypi.org/project/captcha/)**: A Python library for generating and verifying CAPTCHA images, used for enhancing security in user registration and login processes.
- **[Kivy](https://kivy.org/#home)**: An open-source Python library for rapid development of applications with innovative user interfaces, including multi-touch apps.
- **[KivyMD](https://kivymd.readthedocs.io/en/latest/)**: A collection of Material Design compliant widgets for use with Kivy, providing modern and responsive UI components.
- **[Kivy-deps.angle](https://pypi.org/project/Kivy-deps.angle/)**: Dependencies for Kivy, specifically for the ANGLE (Almost Native Graphics Layer Engine) backend.
- **[Kivy-deps.glew](https://pypi.org/project/Kivy-deps.glew/)**: Dependencies for Kivy, specifically for the OpenGL Extension Wrangler Library (GLEW) backend.
- **[Kivy-deps.sdl2](https://pypi.org/project/Kivy-deps.sdl2/)**: Dependencies for Kivy, specifically for the Simple DirectMedia Layer (SDL2) backend.
- **[unittest](https://docs.python.org/3/library/unittest.html)**: A Python library designed for helping with testing, specifically we used it for unit testing
- **[pytest](https://docs.pytest.org/en/8.2.x/)**: A similar testing library used for all types of testing
- **[geopy](https://geopy.readthedocs.io/en/stable/)**: used specifically for finding locations based on coordinates for our adverts

### Resources
Other resources or applications used alongside the project:
- **[DBeaver DBMS Tool](https://dbeaver.io/)**: A free multi-platform database tool for developers, database administrators, analysts, and all people who need to work with databases.
- **[MySQL Relational Database Management System](https://www.mysql.com/)**: An open-source relational database management system.
- **[Git/GitHub](https://github.com/)**: Git is a distributed version control system; GitHub is a platform for hosting and collaborating on Git repositories.
- **[Hand Drawn Profile Icons Pack](https://www.freepik.com/free-vector/hand-drawn-different-profile-icons-pack_17863151.htm)**: A set of free, hand-drawn profile icons used for user avatars.
- **[Hamburger free icon](https://www.flaticon.com/free-icon/hamburger_2203132?term=burger&related_id=2203132)**: A free, hamburger icon used for the placeholder food image
- **[GIMP](https://www.gimp.org/)**: The GNU Image Manipulation Program, a free and open-source raster graphics editor used for image editing and creation.
- **[Pattern Ninja](https://patterninja.com/)**: An online tool for creating patterns, used for designing general advert image
- **[Canva](https://www.canva.com/)**: An online tool for graphical design specifically used to design the logo.png
---
## Testing Documentation

Throughout the testing stage of the project, we adhered closely to our established testing methodology. We employed a combination of static and dynamic tests, with a focus on functional testing using the `unittest` library. These unit tests formed the core of our testing efforts, thoroughly covering individual functions.

To complement this, we conducted integration tests for functions interacting with our database to ensure seamless operation. Additionally, given the significance of the Kivy framework in our project, we performed User Interface (UI) testing. This involved manually operating the program and documenting any issues encountered, ensuring the frontend implementation was robust and user-friendly.

### Testing Methodology Goals Met:

- **Static Testing**: We reviewed the source code in detail, systematically examining each commit to ensure compliance with the specification and compatibility with the overall system.
- **Dynamic Testing**: Functional testing was executed using the `unittest` library, where we created automated tests for various backend functions, including data validation and database operations. These tests were based on the test cases provided **[[HERE]](https://docs.google.com/document/d/1Tkr5HZA3srWEFO2Z04ICSavuXGv-pitTD4o5LDjENt8/edit?usp=sharing) (also available In project submission).**
- **Domain Testing**: We defined a set of inputs required to test each function thoroughly, including valid, extreme, and erroneous data inputs, ensuring correct outputs where returned.
- **Divide and Conquer**: Each team member was assigned specific test cases, regardless of their previous role in the project, leading to a mix of black box and grey box testing. This approach ensured comprehensive coverage and validation of both known and partially known internal structures.

This structured and methodical approach to testing ensured that our program was thoroughly vetted, resulting in a robust, well-performing, and user-friendly application.

**(PLEASE NOTE: Some tests are dependant upon user 64 (TEST_USER) being present in the database, before running test please make sure that said user is present.)** 

---
