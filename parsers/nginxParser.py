import parsers.generic


def parse(line):
    ip = (r''
          '(\d+.\d+.\d+.\d+)\s-\s-\s'
          )
    signature = 'nginx'
    event = parsers.generic.parse(ip, line, signature)
    return event


if __name__ == '__main__':
    pass
