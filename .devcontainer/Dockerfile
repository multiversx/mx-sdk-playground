FROM ubuntu:22.04

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG VERSION_MXPY="v8.1.5"
ARG VERSION_RUST="nightly-2023-05-26"
ARG VERSION_WASM_OPT="version_112"
ARG VERSION_VMTOOLS="v1.4.89"
ARG REPOSITORY_VMTOOLS="https://github.com/multiversx/mx-chain-vm-v1_4-go/archive/{TAG}.tar.gz"
ARG NODE_VERSION=20.9.0

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install some dependencies as root
RUN apt-get update && apt-get install -y \
    wget \ 
    build-essential \
    python3.10 python3-pip python3.10-venv \
    git \
    pkg-config \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Switch to regular user
USER $USERNAME
WORKDIR /home/${USERNAME}

# Create "~/multiversx-sdk"
ENV MULTIVERSX=/home/${USERNAME}/multiversx-sdk
RUN mkdir ${MULTIVERSX}

# Install mxpy
RUN wget -O mxpy-up.py https://raw.githubusercontent.com/multiversx/mx-sdk-py-cli/main/mxpy-up.py && \
    python3 mxpy-up.py --exact-version ${VERSION_MXPY} --not-interactive && \
    rm mxpy-up.py
ENV PATH="${MULTIVERSX}:${PATH}"

# Install rust and other tools
RUN mxpy deps install rust --tag=${VERSION_RUST} && rm -rf ${MULTIVERSX}/vendor-rust/registry/*
RUN mxpy deps install wasm-opt --tag=${VERSION_WASM_OPT} && rm ${MULTIVERSX}/*.tar.gz
RUN mxpy config set "dependencies.vmtools.tag" ${VERSION_VMTOOLS}
RUN mxpy config set "dependencies.vmtools.urlTemplate.linux" ${REPOSITORY_VMTOOLS}
RUN mxpy deps install vmtools && rm ${MULTIVERSX}/*.tar.gz && sudo rm -rf ${MULTIVERSX}/golang

# Install test wallets
RUN mxpy deps install testwallets && rm ${MULTIVERSX}/*.tar.gz

ENV PATH="${MULTIVERSX}/vendor-rust/bin:${MULTIVERSX}/vmtools:${PATH}"
ENV CARGO_HOME="${MULTIVERSX}/vendor-rust"
ENV RUSTUP_HOME="${MULTIVERSX}/vendor-rust"

RUN rustup component add rustfmt && rm -rf ${MULTIVERSX}/vendor-rust/registry/*

# Install node
RUN wget -O install.sh https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh && \
    chmod +x install.sh && \
    ./install.sh
ENV NVM_DIR=/home/${USERNAME}/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/home/${USERNAME}/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
