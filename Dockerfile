FROM public.ecr.aws/docker/library/python:3.10.12
WORKDIR /kabum-product-search

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=127.0.0.1"]