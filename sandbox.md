### Javascript snippets

The folder `snippets-javascript` contains a few Javascript scripts (examples) that can be used to interact with the network and with some test contracts. Feel free to add more scripts, or to add more functionality to the existing ones.

```
node $SNIPPETS_JS/adder.js deploy --bytecode=$SANDBOX/adder.wasm
node $SNIPPETS_JS/adder.js add --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh --value=7
node $SNIPPETS_JS/adder.js get-sum --contract=erd1qqqqqqqqqqqqqpgql5sllxejp8a9qzcn5qh6uvgqgk349p9ysv7sq26xhh
```
