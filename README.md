# mx-sdk-playground

Playground for contracts and dApps.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/multiversx/mx-sdk-playground/tree/init?quickstart=1)

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/multiversx/mx-sdk-playground/tree/init)

## Getting started

Once the devcontainer is started (in VSCode or GitHub Codespaces), run `File > Open Workspace from File` and select the file `.devcontainer/default.code-workspace`. The window will reload and you will be ready to go:

 - Explorer the `Smart Contracts` folder, follow the `README.md` file, then create, build, test and deploy contracts.
 - Explorer the `Frontend` folder, follow the `README.md` file, then create and start dApps.

## For maintainers

Skip this section if you are not a maintainer of the Playground.

Build the Docker image:

```
docker build --network=host . -t multiversx/development-playground:latest -f ./.devcontainer/Dockerfile
```

Push the Docker image:

```
docker push multiversx/development-playground:latest
```
