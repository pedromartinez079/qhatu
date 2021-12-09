FROM python

WORKDIR /qhatu

COPY . /qhatu

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["python","qhatu.py"]

# Image example:
# docker build -t pedromartinez079/qhatu:0.0.1 .
# Container example:
# docker run -d --rm --env-file ../env-files/.information-qhatu --name qhatu pedromartinez079/qhatu:0.0.1
# docker push pedromartinez079/qhatu:0.0.1
