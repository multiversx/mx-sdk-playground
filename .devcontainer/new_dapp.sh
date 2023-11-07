NAME=$1

git clone --depth=1 --branch=main https://github.com/multiversx/mx-template-dapp.git $FRONTEND/$NAME && \
    rm -rf $FRONTEND/$NAME/.git && rm -rf $FRONTEND/$NAME/.gitignore && rm -rf $FRONTEND/$NAME/.github && rm -rf $FRONTEND/$NAME/workflows && \
    rm -rf $FRONTEND/$NAME/cypress && rm -rf $FRONTEND/$NAME/cypress.config.ts
