[![Heroku](http://heroku-badge.herokuapp.com/?app=bctt&style=flat&svg=1)]

Busines Class Table Tennis Wellington
=====================================

Website for the TT business league in Wellington NZ. Available at [bctt.nz](http://bctt.nz)

## Basic setup

```
  $ cd [my-dev-environment]
  $ git clone git@github.com:jordij/bctt.nz.git
  $ cd bctt.nz
  $ vagrant up
  [..... wait until everything gets installed.]
  $ vagrant ssh
  $ djrun
```

Your instance is up and running! Available on **http://localhost:8111**

Backend based on [Wagtail CMS](https://wagtail.io)

Frontend based on [Twitter Bootstrap](http://getbootstrap.com) and [Flat UI Theme](http://designmodo.github.io/Flat-UI/).
