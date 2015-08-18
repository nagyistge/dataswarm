FROM

MAINTAINER David Jonasson david.r.jonasson@gmail.com

ADD /dataswarm /dataswarm

WORKDIR /dataswarm

RUN pip install -r /dataswarm/requirements.txt

EXPOSE 5000

CMD python dataswarm.py
