FROM python:3.11.6
COPY ./req.txt .
RUN pip install -r ./req.txt
COPY . .
CMD ["uvicorn", "project:app","--host", "0.0.0.0", "--port", "8000", "--reload"]