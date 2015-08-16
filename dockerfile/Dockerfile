FROM python

RUN git clone git@gitlab.meltwater.com:platform-test/dataswarm.git

RUN pip install -r /dataswarm/requirements.txt

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /dataswarm

# Set the default command to execute
CMD python dataswarm.py