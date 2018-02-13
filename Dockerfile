# Author James Etheredge

FROM centos:7
ENV container docker

# prep configuring python and pip
RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python
RUN yum -y install python-setuptools
RUN yum -y install python-pip python-wheel
RUN yum -y install python36
RUN yum -y install python36u-pip
RUN pip install --upgrade pip
RUN pip3.6 install --upgrade pip
RUN pip3.6 install --upgrade avro-python3
RUN pip3.6 install --upgrade argparse


# add files
RUN cd
RUN mkdir ArmedSpiderMonkey
RUN mkdir ArmedSpiderMonkey/dataOutput
ADD data_generator.py ArmedSpiderMonkey/
COPY data/ ArmedSpiderMonkey/data
COPY schemas/ ArmedSpiderMonkey/schemas
