pip install -r req.txt


docker build . -t db-project
docker run -it -p 8000:8000 db-project

Start app
uvicorn project:app --reload