# set the base image 
FROM nvidia/cuda:11.1.1-devel-ubuntu20.04 AS dependencies
ARG conda_env=env

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

RUN apt-get update -y                                                       \
    && apt-get install -y --no-install-recommends --no-install-suggests     \
    wget                                                                    \
    git                                                                     \
    chromium-browser                                                        \
    unzip                                                                   \
    pip

RUN apt-get install git-lfs                                                 \
    && git lfs install --skip-repo --skip-smudge

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  -O /tmp/Miniconda3-latest-Linux-x86_64.sh   \
    && /bin/bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda     \
    && rm -rf /tmp/Miniconda3-latest-Linux-x86_64.sh         

ENV PATH=/opt/conda/bin:$PATH
RUN conda update conda \
    && conda create -n $conda_env python=3.7.16 -y

ENV PATH /opt/conda/envs/env/bin:$PATH
ENV CONDA_DEFAULT_ENV env

# RUN conda init bash
# RUN echo "conda activate $conda_env" >> ~/.bashrc

## MAKE ALL BELOW RUN COMMANDS USE THE NEW CONDA ENVIRONMENT
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

RUN apt-get install build-essential -y      \
    && apt-get update -y

# RUN pip install cython                                                      \
#     && pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome-stable_current_amd64.deb \
    && apt-get -f install /tmp/google-chrome-stable_current_amd64.deb -y      \
    && rm -rf /tmp/google-chrome-stable_current_amd64.deb
                         

RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -O /tmp/chromedriver.zip    \
    && rm -rf /usr/bin/chromedriver                                                                                     \
    && rm -rf /usr/bin/LICENSE.chromedriver                                                                             \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ && rm -rf /tmp/chromedriver.zip                                         \
    && chown root:root /usr/bin/chromedriver                                                                            \
    && chmod +x /usr/bin/chromedriver

RUN pip install cryptography==38.0.4
RUN conda install typing_extensions
RUN pip install torch==1.9.0 torchvision -f 'https://download.pytorch.org/whl/cu111/torch_stable.html'
RUN pip install detectron2 -f 'https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.9/index.html'
  
WORKDIR /code
COPY . /code

RUN pip install -r requirements.txt

RUN git clone https://github.com/LamThanhNgan/Phishpedia.git                                        \
    && cd Phishpedia                                                                                \
    && git checkout lamthanhngan/deploy                                                             \
    && cd ..                                                                                        \
    && gdown --folder "https://drive.google.com/drive/folders/1rCEqhu1CS8tphwDKoxsCRh5t1PXfSceH"    \
    && cp -r phishpedia_models/detectron2_pedia/* Phishpedia/phishpedia/src/detectron2_pedia        \     
    && cp -r phishpedia_models/siamese_pedia/* Phishpedia/phishpedia/src/siamese_pedia              \   
    && rm -rf phishpedia_models 

# # INSTALL PHISHPEDIA ...
RUN pip install -e Phishpedia 

CMD python ./manage.py migrate                      \
    && python ./manage.py runserver 0.0.0.0:8000
