# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our app is a trusted second-hand marketplace exclusively for students, where verified student accounts can safely buy, sell, and exchange items within their campus community — saving money, earning cash, and supporting sustainability.


## User stories

This is the link to the Issues page: https://github.com/swe-students-fall2025/2-web-app-great/issues

## Steps necessary to run the software

1. cd LoopU_Final_Complete


2. Create and activate a virtual environment

    python3 -m venv venv

    if macOS / Linux：

    source venv/bin/activate

    if Windows：

    venv\Scripts\activate


3. Install dependencies

    pip install -r requirements.txt


4. Configure environment variables

    cp env.example .env

    Edit .env if needed. Example:

    MONGO_URI="mongodb://localhost:27017/loopu"

    SECRET_KEY="your_secret_key_here"


5. Start MongoDB

   Option 1: Local MongoDB (with config file)

   1. Create a config file (for example, `mongod.conf`):

      macOS / Linux
      nano mongod.conf

      Windows (PowerShell)
      notepad mongod.conf

   2. Paste the following minimal configuration into the file:

      systemLog:
        destination: file
        path: ./mongo.log
        logAppend: true
      storage:
        dbPath: ./data
      net:
        bindIp: 127.0.0.1
        port: 27017

   3. Start MongoDB with this config file:
      mongod --config mongod.conf

   Option 2: MongoDB Atlas (Optional)
   - If you don’t want to install MongoDB locally, you can set up a free cluster on https://www.mongodb.com/atlas/database and replace the `MONGO_URI` in `.env` with your Atlas connection string.


6. Run the Flask application

python app.py

Expected output:

Running on http://127.0.0.1:5050


7. Open the app in your browser

open http://127.0.0.1:5050    # macOS

start http://127.0.0.1:5050   # Windows


8. Front-end testing tip

Should view with inspect on 14 Pro Max mobile viewport



## Task boards
Sprint 1: https://github.com/orgs/swe-students-fall2025/projects/28

Sprint 2: https://github.com/orgs/swe-students-fall2025/projects/29

User Story Status Board: https://github.com/orgs/swe-students-fall2025/projects/56
