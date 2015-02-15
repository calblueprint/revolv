RE-volv
================

This application allows RE-volv to crowdfund donations to community solar projects in order to spread green energy and save the planet.

Stage URL: http://revolv-stage.herokuapp.com/

Who We Are
----------
![bp](http://bptech.berkeley.edu/assets/logo-full-large-d6419503b443e360bc6c404a16417583.png "BP Banner")
**[Cal Blueprint](http://www.calblueprint.org/)** is a student-run UC Berkeley organization devoted to matching the skills of its members to our desire to see social good enacted in our community. Each semester, teams of 4-5 students work closely with a non-profit to bring technological solutions to the problems they face every day.


Installation
------------

You can choose to use [vagrant](http://vagrantup.com) or not.

If *not* using vagrant:

    $ ./bootstrap.sh
    $ python manage.py migrate
    $ npm install -g grunt-cli
    $ npm install
    $ npm install -g bower
    $ cd revolv/static/ && bower install foundation && cd ../../
    $ grunt sass
    $ python manage.py migrate
    $ python manage.py runserver

If *using* vagrant:

1. Install Virtualbox
2. Install vagrant
3. `vagrant up --provision`
4. python vmanage.py migrate
5. python vmanage.py runserver

Development
-----------
1. Running `grunt watch` will start a process which will watch for changes to specific SCSS files (defined in `Gruntfile`) and will autocompile them to CSS.
