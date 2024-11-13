# server-sent-event-demo
server sent event demo project to know how sse works along with RESTApis


## Pre-requisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- Python 3.10 (for virtual enviornment)

## Installation & usage with docker

##### Step 1: Clone the repository
```bash
git clone {repo_url}
cd sse-demo
```

##### Step 2: Configure .env

##### Step 3: Build the docker image
```bash
docker build -t sse-demo-app .
```

##### Step 4: Run the docker container
```bash
docker run -d -p 8000:8000 sse-demo-app
```

## Installation & usage without docker

##### Step 1: Clone the repository
```bash
git clone {repo_url}
cd sse-demo
```

##### Step 2: Configure .env

##### Step 3: Create & activate virtual-environment
```bash
python3 -m venv env-name
source env-name/bin/activate
```

##### Step 4: Install requirements
```bash
pip install --no-cache-dir -r requirements.txt
```

##### Step 4: Run application
```bash
python main.py
```

## Usage
- open [home_url](http://0.0.0.0:8000/api/v1/) to start new process
- pick task_id from homepage & change status using [this_api](http://localhost:8000/docs#/default/update_status_api_v1_task__task_id__status_post)
- moniter changes in [home_url](http://0.0.0.0:8000/api/v1/)


#### EnjoyCoding!!!
