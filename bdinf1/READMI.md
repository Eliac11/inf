pip install -r req.txt


docker build . -t dbproject
docker run -it -p *порт*:*порт* -e DB_CONNECT_STRING=**username**:**password**@**ipdb**/**dbname** dbproject 

Start app
uvicorn project:app --reload