FROM ubuntu:22.04

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG MXPY_VERSION="v8.1.5"
ARG RUST_VERSION="nightly-2023-05-26"
ARG WASM_OPT_VERSION="version_112"
ARG VMTOOLS_VERSION="v1.4.89"
ARG VMTOOLS_REPOSITORY="https://github.com/multiversx/mx-chain-vm-v1_4-go/archive/{TAG}.tar.gz"
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
    python3 mxpy-up.py --exact-version ${MXPY_VERSION} --not-interactive && \
    rm mxpy-up.py
ENV PATH="${MULTIVERSX}:${PATH}"

# Install rust and other tools
RUN mxpy deps install rust --tag=${RUST_VERSION} && rm -rf ${MULTIVERSX}/vendor-rust/registry/*
RUN mxpy deps install wasm-opt --tag=${WASM_OPT_VERSION} && rm ${MULTIVERSX}/*.tar.gz
RUN mxpy config set "dependencies.vmtools.tag" ${VMTOOLS_VERSION}
RUN mxpy config set "dependencies.vmtools.urlTemplate.linux" ${VMTOOLS_REPOSITORY}
RUN mxpy deps install vmtools && rm ${MULTIVERSX}/*.tar.gz && sudo rm -rf ${MULTIVERSX}/golang

# Install test wallets
RUN mxpy deps install testwallets && rm ${MULTIVERSX}/*.tar.gz

ENV PATH="${MULTIVERSX}/vendor-rust/bin:${MULTIVERSX}/vmtools:${PATH}"
ENV CARGO_HOME="${MULTIVERSX}/vendor-rust"
ENV RUSTUP_HOME="${MULTIVERSX}/vendor-rust"

RUN rustup component add rustfmt && rm -rf ${MULTIVERSX}/vendor-rust/registry/*

# Install Node JS
RUN wget -O install.sh https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh && \
    chmod +x install.sh && \
    ./install.sh
ENV NVM_DIR=/home/${USERNAME}/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/home/${USERNAME}/.nvm/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install MultiversX libraries (Python)
ARG PY_SDK_CORE_VERSION="0.7.1"
ARG PY_SDK_WALLET_VERSION="0.8.2"
ARG PY_SDK_NETWORK_PROVIDERS_VERSION="0.12.1"

RUN pip3 install multiversx-sdk-core==${PY_SDK_CORE_VERSION} && \
    pip3 install multiversx-sdk-wallet==${PY_SDK_WALLET_VERSION} && \
    pip3 install multiversx-sdk-network-providers==${PY_SDK_NETWORK_PROVIDERS_VERSION}

# Install MultiversX libraries (JavaScript)
ARG JS_SDK_CORE_VERSION="v12.12.0"
ARG JS_SDK_WALLET_VERSION="v4.2.0"
ARG JS_SDK_NETWORK_PROVIDERS_VERSION="v2.0.0"

RUN npm install -g @multiversx/sdk-core@${JS_SDK_CORE_VERSION} && \
    npm install -g @multiversx/sdk-wallet@${JS_SDK_WALLET_VERSION} && \
    npm install -g @multiversx/sdk-network-providers@${JS_SDK_NETWORK_PROVIDERS_VERSION} \
    npm install -g yarn
