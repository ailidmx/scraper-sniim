FROM python:3.8

RUN mkdir precios
COPY . precios/

WORKDIR /precios
RUN pip install -r requirements.txt && ls && chmod 777 start.sh

ENTRYPOINT ["python setup.py install;python sniim/cli.py  --historial"] 