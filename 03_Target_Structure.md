VONNEU/  <--  main project folder
├── app.py                <-- Creates and configures the Flask app
├── config.py             <-- Configuration settings
├── requirements.txt     <-- Project dependencies
├── .env                  <-- Environment variables
├── static/              <-- Static assets (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── scripts.js
├── templates/           <-- HTML templates
│   ├── base.html         <-- Base template
│   ├── macros.html      <-- Jinja macros
│   ├── probes/           <-- Templates for the probes Blueprint
│   │   ├── list.html
│   │   └── details.html
│   └── asteroids/        <-- Templates for the asteroids Blueprint
│       ├── index.html
│       └── ...
├── views/                <-- Presentation logic (views/controllers)
│   ├── __init__.py
│   ├── probes.py         <-- Probes Blueprint
│   └── asteroids.py     <-- Asteroids Blueprint
├── models/               <-- Database models (SQLAlchemy)
│   ├── __init__.py
│   ├── probe.py         <-- Probe model
│   └── asteroid.py      <-- Asteroid model
└── utils/                <-- Utility functions
    ├── __init__.py
    └── db.py              <-- Database connection management
