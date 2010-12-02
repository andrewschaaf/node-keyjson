
keyjson = require('./keyjson')

#### Data

BYTESTRINGS = [
    Buffer([]), 
    Buffer([0]), 
    Buffer([0, 1]), 
    Buffer([0, 1, 2]), 
    Buffer([0, 1, 2, 3])
]

octets = []
for n in range(5):
    for i in range(256):
        octets.push(i)
BYTESTRINGS.push(Buffer(octets))


KEYJSON_EXAMPLES = [
    [['x', 0], 'NTR4AMCA'],
    [None, 'MQ=='],
    [False, 'Mg=='],
    [True, 'Mw=='],
    ['Montréal', 'NE1vbnRyw6lhbA=='],
    [['x', 0], 'NTR4AMCA'],
    [['x', 0, 'Foo'], 'NTR4AMCAADRGb28='],
    [{'y': 'Foo', 'x': 0}, 'NjR4AMCAADR5ADRGb28='],
    [-16384, 'vf7//w=='],
    [-129, 'vv7+'],
    [-128, 'vv7/'],
    [-127, 'v4A='],
    [-126, 'v4E='],
    [-2, 'v/0='],
    [-1, 'v/4='],
    [0, 'wIA='],
    [1, 'wIE='],
    [126, 'wP4='],
    [127, 'wP8='],
    [128, 'wYGA'],
    [129, 'wYGB'],
    [16384, 'woGAgA=='],
    [2097152, 'w4GAgIA=']
]


#### Tests

def fatalError(x):
    msg = JSON.stringify(x)
    print(msg)
    raise Exception(msg)

def assertBuffersEqual(x, y, note):
    s1 = x.toString('binary')
    s2 = y.toString('binary')
    if s1 != s2:
        fatalError(['Buffers not equal:', s1, s2, 'note:', note])

def assertEquivalent(x, y, note):
    
    t = typeof(x)
    x2 = JSON.parse(JSON.stringify(x))
    y2 = JSON.parse(JSON.stringify(y))
    
    if (
            x == True or
            x == False or
            x == None or
            t == 'string' or
            t == 'number' or 
            isinstance(x, Array)):
        if JSON.stringify(x) != JSON.stringify(y):
            fatalError(['Not equal:', x, y, 'note:', note])
    
    else:
        for k in dict(x2):
            assertEquivalent(x[k], y[k], note)
        for k in dict(y2):
            if not (k in x):
                fatalError(['Key', k, 'from', y2, 'not found in', x, 'note:', note])


def test64():
    for x in BYTESTRINGS:
        y = keyjson.b64encode(x)
        x2 = keyjson.b64decode(y)
        assertBuffersEqual(x, x2, y)


def testExamples():
    for tup in KEYJSON_EXAMPLES:
        x = tup[0]
        y_expected = Buffer(tup[1], 'base64')
        
        y = keyjson.stringify(x)
        assertBuffersEqual(y, y_expected, x)
        x2 = keyjson.parse(y)
        assertEquivalent(x, x2, y)


test64()
testExamples()

print('OK')

