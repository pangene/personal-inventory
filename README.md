# Personal Inventory Tracker

## Introduction

This repository is for a learning side-project to develop a personal inventory tracker using Django and React. 

This project uses a hybrid structure, where the React is integrated into the Django project and interacts with the database through a RESTful API made with the Django REST framework. (See Architecture for more detail)

A demo for this project is deployed with Heroku, and is hosted at https://personalinventorytracker.herokuapp.com/.

## Installation

For hosting on your local machine, follow these instructions on your terminal:

1. Clone the repository onto your local machine with:

`> git clone git@github.com:pangene/personal-inventory.git`

2. Move into your directory with 

`> cd personal-inventory`

3. Install the necessary python packages with

```
> python -m venv venv
> source venv/bin/activate    <-- Note activating virtual envs on Windows is different
> pip install -r requirements.txt
```
Note that the first two steps just set up a virtual environment, and are optional.

4. Install the necessary node packages with

`> npm install`

5. Run the following commands to prepare the project

```
> npm run dev   <-- Bundles into index-bundle.js in static folder. Optionally, npm run build to bundle for production.
> python manage.py migrate
```

6. Start the server with

`> python manage.py runserver`

Now, the development server should be accessible from http://127.0.0.1:8000/.

## Architecture

Below is an annotated folder structure (excluding files) of this github repo.

```
.   <-- Django project 
├── accounts    <-- Django app for all accounts/authentication stuff
│   ├── migrations
│   └── tests
├── frontend    <-- Frontend folder for the home React page (see below)
│   └── components
├── inventory   <-- Django app for all inventory stuff
│   ├── migrations
│   └── tests
├── myinventory     <-- Django config folder
├── static  <-- Django static resources folder
│   ├── css
│   ├── images
│   ├── js
│   └── webfonts
└── templates   <-- all templates used by Django, contains some base/include only html files as well
    ├── inventory   <-- all templates for inventory, including anchor for the React frontend
    └── registration    <-- all templates for accounts stuff
```

Note the above annotated architecture only includes the folders, and some basic knowledge of a Django project's typical file structure is expected.

As mentioned prior, this project uses a 'hybrid' structure for Django-React. This means that the frontend and backend are not completely decoupled. While perhaps not suitable for a large-scale project, this allows us to use many of Django's powerful 'batteries-included' built-in features, while also adding a bit of modern responsiveness.

This hybrid structure means that the React frontend anchors into the Django templates as it would when adding React to any html file. It interacts with the Django database with a RESTful API made with the Django REST Framework, with the serializers and views for the API found in the `inventory/` folder.

Also, note that in the frontend, there is a components folder, but no styles folder. This differs from a proper React frontend, where components and styles are linked together so they are easily reusable. This is because the focus of this learning project was much more about the Django backend than the frontend. (Alternatively, it's because I didn't know that when I started.)

## TODOS/Improvements

- If you poke around the internals, you'll notice that the Item model includes a upc field. UPC stands for Universal Product Code, and it's because originally, I wanted to let the user scan bar codes. I had some trouble finding a good API for the UPC lookup though.

- The frontend aspect, as noted in the architecture, is messy. I have only one styles.css for all my personal styling, which makes things fairly disorganized.

- I use email as username. I should require an email to be sent to authorize accounts.

- User profile and User authentication would ideally be separated.
