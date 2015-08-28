import parsers.generic


def parse(line):
    ip = (r''
          '(\d+.\d+.\d+.\d+)\s-\s-\s'
          )
    event = parsers.generic.parse(ip, line)
    return event


if __name__ == '__main__':
    pass
