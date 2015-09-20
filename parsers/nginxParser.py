import parsers.generic


def parse(line):
    ipregex = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'
               )
    signature = 'web server request'
    event = parsers.generic.parse(ipregex, line, signature)
    return event


if __name__ == '__main__':
    pass
