## What is keyjson?

See [http://keyjson.org](http://keyjson.org)

## Installing

_(TODO: support <code>npm install node-keyjson</code>)_

<code>keyjson.js</code> is self-contained and you can install it however you like.

One option (if you're already using npm):

<pre>mkdir /usr/local/lib/node/keyjson
ln -s /...keyjson.js /usr/local/lib/node/keyjson/index.js
</pre>

Note that the path to keyjson.js must be absolute.

## Using

<pre>keyjson = require('keyjson');
buf = keyjson.stringify(['enwiki', 'Hacker News', 1729000]);
keyjson.parse(buf);
</pre>


## Building (optional)

#### Prereqs

* [PYXC-PJ](http://pyxc.org) (with its repo on your <code>PYTHONPATH</code>)
* [Closure Compiler](http://code.google.com/closure/compiler/) (with <code>CLOSURE_JAR</code> pointing to its .jar)

<pre>python make.py
node test.js
</pre>
