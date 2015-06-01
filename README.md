RE-volv
================

This application allows [RE-volv](http://re-volv.org) to crowdfund donations to community solar projects in order to promote renewable energy and help save the planet. Learn more about Blueprint's work with RE-volv [on our blog](https://medium.com/@blueprint/power-to-the-people-44e13a5a55c5).

Staging URL: http://revolv-stage.herokuapp.com/

![Codeship](https://codeship.com/projects/45c89d50-af15-0132-a36c-2a23891ee2d0/status?branch=master)

Who We Are
----------
![bp](http://bptech.berkeley.edu/assets/logo-full-large-d6419503b443e360bc6c404a16417583.png "BP Banner")
**[Cal Blueprint](http://www.calblueprint.org/)** is a student-run UC Berkeley organization devoted to matching the skills of its members to our desire to see social good enacted in our community. Each semester, teams of 4-5 students work closely with a non-profit to bring technological solutions to the problems they face every day.


Installation
------------

You can choose to use [vagrant](http://vagrantup.com) or not. Note that in either case, you will need to acquire Paypal and Amazon API keys from one of the maintainers, or the app will not work locally.

If *not* using vagrant, first install PostgreSQL and set up a database and user with the credentials in the `DATABASES` setting from revolv/settings.py. Then:

    $ pre-commit install
    $ npm install -g grunt-cli
    $ npm install -g bower
    $ npm install
    $ bower install
    $ grunt sass
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py runserver
    $ python manage.py seed

If *using* vagrant:

1. Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
2. Install [vagrant](https://www.vagrantup.com/)
3. `vagrant up --provision`
4. `python vmanage.py migrate`
5. `python vmanage.py runserver`
6. `python vmanage.py seed`

Development
-----------
1. Running `grunt watch` will start a process which will watch for changes to specific SCSS files (defined in `Gruntfile`) and will autocompile them to CSS.
2. You can use the `vmanage.py` script to run manage.py commands on the running vagrant machine without having to `vagrant ssh` in. For example: `python vmanage.py runserver`, `python vmanage.py migrate`, `python vmanage.py makemigrations --empty`, etc.
3. You can run `manage.py seed` to seed the database, and you can run `manage.py seed --clear` to clear the seeded data (useful for when something goes wrong and you want to regenerate all the seed data from scratch). You can also run `manage.py seed revolvuserprofile` to seed specific data (replace `revolvuserprofile` with any of the strings from `revolv/base/management/commands/seed.py`).

Contributing
------------
All of Blueprint's work is open source and we welcome contributions. If you would like to contribute to work on this project, please open an issue and we'll work to get your environment set up.
