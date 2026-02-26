FROM ubuntu:24.04

ARG USERNAME=ubuntu
ARG VERSION_MXPY="11.3.1"
ARG SDK_PY_VERSION="2.4.0"
ARG VERSION_RUST="1.90.0"
ARG VERSION_SC_META="0.64.2"
ARG VERSION_NODE=22

ENV DEBIAN_FRONTEND=noninteractive

# Base system dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    python3 \
    python3-venv \
    python3-pip \
    pipx \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Give sudo access
RUN echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Environment variables
ENV MULTIVERSX="/home/${USERNAME}/multiversx-sdk"
ENV NVM_DIR="/home/${USERNAME}/.nvm"
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
ENV PATH="/home/${USERNAME}/.cargo/bin:${PATH}"

# Python virtual environment and SDK installation
RUN python3 -m venv /home/${USERNAME}/venv
ENV PATH="/home/${USERNAME}/venv/bin:${PATH}"

RUN pip install --upgrade pip \
    && pip install multiversx-sdk==${SDK_PY_VERSION}

# Install mxpy via pipx
RUN pipx install multiversx-sdk-cli==${VERSION_MXPY}

# Install Rust
RUN curl https://sh.rustup.rs -sSf | \
    sh -s -- -y --profile minimal --default-toolchain ${VERSION_RUST}

# Install sc-meta tools
RUN cargo install multiversx-sc-meta --version ${VERSION_SC_META} --locked \
    && sc-meta install all

# Install test wallets
RUN mxpy deps install testwallets

# Install Node.js via nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

RUN bash -c "source $NVM_DIR/nvm.sh \
    && nvm install ${VERSION_NODE} \
    && nvm alias default ${VERSION_NODE}"

ENV PATH="$NVM_DIR/versions/node/v${VERSION_NODE}/bin:${PATH}"

# -------------------------------------------------
RUN echo 'export PATH="$HOME/venv/bin:$PATH"' >> ~/.bashrc \
    && echo 'if [ -f "$HOME/venv/bin/activate" ]; then source "$HOME/venv/bin/activate"; fi' >> ~/.bashrc \
    && echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc

CMD ["bash"]
