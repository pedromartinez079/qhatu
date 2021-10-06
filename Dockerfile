FROM python

WORKDIR /qhatu

COPY . /qhatu

RUN pip3 install -r requirements.txt

CMD ["python","qhatu.py"]

# Image example:
# docker build -t pedromartinez079/qhatu:0.0.1 .