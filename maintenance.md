# mx-sdk-playground - maintenance

Skip this if you are not a maintainer of the Playground.

Build the Docker image:

```
docker build --network=host . -t multiversx/development-playground:latest -f ./.devcontainer/Dockerfile
```

Push the Docker image:

```
docker push multiversx/development-playground:latest
```
