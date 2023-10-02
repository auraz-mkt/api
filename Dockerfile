# Arguments to configure Python
ARG PYTHON_VERSION=3.11.7

################################################################################
##                                BUILD IMAGE                                 ##
################################################################################

# Create build image
FROM python:${PYTHON_VERSION} AS build

# Arguments to configure Pip
ARG PIP_VERSION=23.2.1
ARG POETRY_VERSION=1.6.1

# Arguments to build API
ARG API_WORKDIR=/usr/src/auraz
ARG API_USER=auraz
ARG API_UID=1000
ARG API_GID=1000

# Set API mode (with/without autoreload)
ENV API_MODE="development"

# Metadata about the project
LABEL br.com.auraz.authors="auraz.mkt+dev@gmail.com"

# Set api directory
WORKDIR ${API_WORKDIR}

# Create non-privilleged user to run application
# and give it proper permissions over the workdir
RUN groupadd --gid ${API_GID} ${API_USER} \
    && useradd --uid ${API_UID} --gid ${API_GID} -m ${API_USER} \
    && chown -R ${API_UID}:${API_GID} ${API_WORKDIR}

# Copy list of OS dependencies
COPY packages.txt ./

# Install OS packages
RUN apt-get -qq update && xargs apt-get -qq -y install < packages.txt

# Set pip"s standard version
RUN pip install pip==${PIP_VERSION} poetry==${POETRY_VERSION}

# Run API as unprivilleged user
USER ${API_USER}

# Copy list of Python dependencies
COPY --chown=${API_USER} poetry.toml pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install

# Copy source code
COPY --chown=${API_USER} . .

# Install project
RUN poetry install

# Run API
CMD ["poetry", "run", "python", "-m", "auraz.api"]
