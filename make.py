

import pj.api

def main():
    
    for name, closureMode in (
            ('keyjson', 'advanced'),
            ('test', 'simple')):
        
        with open('src/%s.py' % name, 'rb') as f:
            py = unicode(f.read(), 'utf-8')
        
        js = pj.api.codeToCode(py)
        
        js = '(function(){%s})();' % js
        
        js = pj.api.closureCompile(js, closureMode)
        
        with open('%s.js' % name, 'wb') as f:
            f.write(js.encode('utf-8'))


if __name__ == '__main__':
    main()
