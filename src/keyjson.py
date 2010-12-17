
#### Constants

NULL = 0x31
FALSE = 0x32
TRUE = 0x33
UNICODE = 0x34
LIST = 0x35
DICT = 0x36

NULL_STR = '1'
FALSE_STR = '2'
TRUE_STR = '3'
UNICODE_STR = '4'
LIST_STR = '5'
DICT_STR = '6'

LIST_DELIMITER = 0x00

BASE64_ALPHABET = '()0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!'
BASE64_ALPHABET_PADDING_1 = '!'
BASE64_ALPHABET_PADDING_2 = '!!'


#### {en,de}code_int


def encode_int(n):
    
    # Notes:
    # * JavaScript's number cannot represent all integers for sizes 9 and 10
    # * Closure Compiler Advanced Mode doesn't optimize "Math.pow(128, 2)"!
    
    if n >= 0:
        if n < 128:          size = 1
        elif n < 16384:        size = 2
        elif n < 2097152:        size = 3
        elif n < 268435456:        size = 4
        elif n < 34359738368:        size = 5
        elif n < 4398046511104:        size = 6
        elif n < 562949953421312:        size = 7
        elif n < 72057594037927936:        size = 8
        else:
            raise ValueError('Number out of bounds')
        
        prefix = (0xC0 - 1) + size
        x = n
    
    else:
        if n > -128:       size = 1
        elif n > -16384:     size = 2
        elif n > -2097152:     size = 3
        elif n > -268435456:     size = 4
        elif n > -34359738368:     size = 5
        elif n > -4398046511104:     size = 6
        elif n > -562949953421312:     size = 7
        elif n > -72057594037927936:     size = 8
        else:
            raise ValueError('Number out of bounds')
        
        prefix = (0xBF + 1) - size
        x = n + (128**size) - 1
    
    data = Buffer(size + 1)
    data[0] = prefix
    rshift = 7 * (size - 1)
    for i in range(1, size + 1):
        data[i] = 128 + ((x >> rshift) & 0x7F)
        rshift -= 7
    
    return data


def decode_int(data):
    
    size = len(data) - 1
    
    x = 0
    lshift = 7 * (size - 1)
    for i in range(size):
        x |= ((data[i + 1] - 128) << lshift)
        lshift -= 7
    
    if data[0] >= 0xC0:
        return x
    else:
        return x - (128**size - 1)


#### stringify / parse

def split_buffer(buf, delim):
    
    slices = []
    leftIndex = 0
    
    # All slices except the last
    for i in range(len(buf)):
        if buf[i] == delim:
            slices.push(buf.slice(leftIndex, i))
            leftIndex = i + 1
    
    # The last slice
    slices.push(buf.slice(leftIndex, len(buf)))
    
    return slices


def join_buffers(buffers, delim, prefixValue):
    
    resultSize = len(buffers)
    for buf in buffers:
        resultSize += len(buf)
    
    result = Buffer(resultSize)
    result[0] = prefixValue
    
    pos = 1
    for buf in buffers:
        buf.copy(result, pos, 0)
        pos += len(buf) + 1
        if pos < resultSize:
            result[pos - 1] = delim
    
    return result


def stringify(x, atomsOnly):
    
    if x == None:     return Buffer(NULL_STR)
    if x == False:    return Buffer(FALSE_STR)
    if x == True:     return Buffer(TRUE_STR)
    
    t = typeof(x)
    
    if t == 'string':
        return Buffer(UNICODE_STR + x)
    
    if t == 'number':
        if not (isFinite(x) and x % 1 == 0):
            raise ValueError("keyjson doesn't support non-integer numbers")
        return encode_int(x)
    
    if atomsOnly:
        raise ValueError("keyjson doesn't support sub-structures")
    
    # So it's a list or a dict.
    
    if isinstance(x, Array):
        arr = [stringify(kid) for kid in x]
        return join_buffers(arr, LIST_DELIMITER, LIST)
    
    else:
        key_tuples = []
        for k in dict(x):
            key_tuples.push([stringify(k), k])
        key_tuples.sort()
        
        interleaved = []
        for tup in key_tuples:
            interleaved.push(tup[0])
            interleaved.push(stringify(x[tup[1]]))
        return join_buffers(interleaved, LIST_DELIMITER, DICT)
    
    raise ValueError('Unsupported prefix')


def parse(data):
    
    if not len(data):
        raise ValueError('Blank input')
    
    prefix = data[0]
    
    if prefix > 0x80:
        return decode_int(data)
    
    if prefix == NULL:   return None
    if prefix == FALSE:   return False
    if prefix == TRUE:   return True
    
    body = data.slice(1, len(data))
    
    if prefix == UNICODE:
        return body.toString('utf-8')
    
    # So it's a list or a dict.
    
    arr = [parse(x) for x in split_buffer(body, LIST_DELIMITER)]
    
    if prefix == LIST:
        return arr
    
    if prefix == DICT:
        d = {}
        for i in range(len(arr)):
            d[arr[2 * i]] = arr[2 * i + 1]
        return d
    
    raise ValueError('Unknown prefix.')


#### b64{en,de}code


def b64encode(octets):
    
    strings = []
    numOctets = len(octets)
    i = 0
    
    while i < numOctets:
        combined = (
                        ((octets[i] or 0) << 16) |
                        ((octets[i + 1] or 0) << 8) | 
                        (octets[i + 2] or 0))
        i += 3
        strings.push(
            BASE64_ALPHABET.charAt((combined >> 18) & 0x3F) + 
            BASE64_ALPHABET.charAt((combined >> 12) & 0x3F) + 
            BASE64_ALPHABET.charAt((combined >> 6) & 0x3F) + 
            BASE64_ALPHABET.charAt((combined) & 0x3F))
    
    s = strings.join('')
    numOctetsMod3 = numOctets % 3
    if numOctetsMod3 == 1:
        s = s.slice(0, -2) + BASE64_ALPHABET_PADDING_2
    elif numOctetsMod3 == 2:
        s = s.slice(0, -1) + BASE64_ALPHABET_PADDING_1
    
    return s


def b64decode(s):
    '''
    Padding is not optional
    '''
    
    if isinstance(s, Buffer):
        s = s.toString('utf-8')
    
    octets = []
    numChars = len(s)
    
    i = 0
    while i < numChars:
        
        i1 = BASE64_ALPHABET.indexOf(s[i])
        i2 = BASE64_ALPHABET.indexOf(s[i + 1])
        i3 = BASE64_ALPHABET.indexOf(s[i + 2])
        i4 = BASE64_ALPHABET.indexOf(s[i + 3])
        i += 4
        
        numPaddingChars = (i3 >> 6) + (i4 >> 6)
        combined = (
            (i1 << 18) |
            (i2 << 12) |
            ((i3 % 64) << 6) |
            ((i4 % 64)))
        
        octets.push((combined >> 16) & 0xFF)
        if numPaddingChars < 2:
            octets.push((combined >> 8) & 0xFF)
        if numPaddingChars < 1:
            octets.push((combined) & 0xFF)
    
    return Buffer(octets)


#### Convenience

def stringify64(x):
    return b64encode(stringify(x))


def parse64(string_or_buf):
    return parse(b64decode(string_or_buf))


#### Exports

exports['stringify'] = stringify
exports['parse'] = parse

exports['b64encode'] = b64encode
exports['b64decode'] = b64decode

exports['stringify64'] = stringify64
exports['parse64'] = parse64

