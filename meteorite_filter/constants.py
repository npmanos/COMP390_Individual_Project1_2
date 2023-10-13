WELCOME_MESSAGE = '''\
Meteorite Data Filter
(c) October 2023 Nick Manos
        
Welcome! This application allows you to filter a provided meteorite data file.

To begin, please type the filename, including its file extension and path if
necessary. (Ex: "meteorite_landings_data.txt") To exit the application, type "?q":\
'''

OPEN_MODES = [
    {
        'param': 'r',
        'desc': 'open for reading',
        'short_desc': 'read'
    },
    {
        'param': 'w',
        'desc': 'open for writing, truncating the file first',
        'short_desc': 'write (truncate)'
    },
    {
        'param': 'x',
        'desc': 'open for exclusive creation, failing if the file already exists',
        'short_desc': 'create'
    },
    {
        'param': 'a',
        'desc': 'open for writing, appending to the end of the file if it exists',
        'short_desc': 'write (append)'
    }
]



OPEN_FORMATS = [
    {
        'param': 't',
        'desc': 'text mode',
        'short_desc': 'text'
    },
    {
        'param': 'b',
        'desc': 'binary mode',
        'short_desc': 'binary'
    }
]

OPEN_SHORT_DESCS = {
    'r': 'read',
    'w': 'write (truncate)',
    'x': 'create',
    'a': 'write (append)',
    't': 'text',
    'b': 'binary'
}
