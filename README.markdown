## What is keyjson?

It's awesome. See [keyjson.org](http://keyjson.org)

## Installing

<pre>
npm install keyjson
</pre>

## Usage / API

*"Software using Semantic Versioning MUST declare a public API. [...]<br>However it is done, it should be precise and comprehensive."*

*"Version 1.0.0 defines the public API"*

The following plus [keyjson.org](http://keyjson.org) should be precise and comprehensive enough:

<pre>
keyjson = require('keyjson');
</pre>

#### {stringify,parse}
<pre>
buffer = keyjson.stringify(['enwiki', 'Hacker News', 1729000]);
x = keyjson.parse(buffer);
</pre>

#### b64{en,de}code
<pre>
string = keyjson.b64encode(buffer_or_array_of_octets);
buffer = keyjson.b64decode(string_or_buffer); // padding is not optional.
</pre>

#### {stringify,parse}64

<pre>
keyjson.stringify64(x) == keyjson.b64encode(
                            keyjson.stringify(x))

keyjson.parse64(sb) == keyjson.parse(
                            keyjson.b64decode(sb))
</pre>

## Developing

#### Prereqs

* [PYXC-PJ](http://pyxc.org) (with its repo on your <code>PYTHONPATH</code>)
* [Closure Compiler](http://code.google.com/closure/compiler/) (with <code>CLOSURE_JAR</code> pointing to its .jar)

<pre>python make.py
node test.js
</pre>
