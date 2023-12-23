from meteorite_filter.output import TerminalOutput, TextFileOutput


WELCOME_MESSAGE = '''\
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃                          METEORITE DATA FILTER                           ┃
  ┃                                                                          ┃
  ┃ Welcome! This application allows you to filter meteorite landing data by ┃
  ┃ mass and year.                                                           ┃
  ┃                                                                          ┃
  ┃ Instructions:                                                            ┃
  ┃   You must provide a file containing the meteorite data in a specific    ┃
  ┃   format. There must be 12 data fields seperated by a tab character. 3   ┃
  ┃   of the 12 fields must be "name", "mass (g)", and "year".               ┃
  ┃                                                                          ┃
  ┃   On-screen instructions are provided to guide you through using the     ┃
  ┃   program. When presented with multiple options, type the number of your ┃
  ┃   choice followed by the enter key. If there is a default option, you    ┃
  ┃   can just press the enter key to select it. You may also type "q" to    ┃
  ┃   exit the application.                                                  ┃
  ┃                                                                          ┃
  ┃                                              (c) October 2023 Nick Manos ┃
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
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

TYPE_MAP = {
    'id': int,
    'mass (g)': float,
    'year': int,
    'reclat': float,
    'reclong': float,
    'States': int,
    'Counties': int
}

FILTER_OPTIONS = {
    'mass (g)': {
        'menu_desc': 'Meteorite mass',
        'input_desc': "the meteorite's mass in grams",
        'header': 'MASS (g)'
    },
    'year': {
        'menu_desc': 'Year meteorite fell',
        'input_desc': 'the year the meteorite fell',
        'header': 'YEAR'
    }
}

OUTPUT_OPTIONS = {
    'terminal': {
        'menu_desc': 'Display on screen',
        'func': TerminalOutput.output
    },
    'text': {
        'menu_desc': 'Save to a text (.txt) file',
        'func': TextFileOutput.output
    }
}
