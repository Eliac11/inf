pip install -r req.txt


docker build . -t dbproject
docker run -it -p 8000:8000 dbproject

Start app
uvicorn project:app --reload