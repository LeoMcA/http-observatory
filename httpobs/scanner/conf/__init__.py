from os import environ, cpu_count

import configparser
import os.path
import sys


# Read in the default config file if /etc/httpobs.conf doesn't already exist
__dirname = os.path.abspath(os.path.dirname(__file__))
_config_parser = configparser.ConfigParser()
_config_parser.read_file(open(os.path.join(__dirname, 'httpobs.conf')))                  # default values
_config_parser.read(['/etc/httpobs.conf', os.path.expanduser('~/.httpobs.conf')])        # overridden values


# Return None if it's not in the config parser
def __conf(section, param, type=None, default=None):
    try:
        if type == str or type is None:
            return _config_parser.get(section, param)
        elif type == int:
            return _config_parser.getint(section, param)
        elif type == bool:
            return _config_parser.getboolean(section, param)
        elif type == float:
            return _config_parser.getfloat(section, param)
        else:
            return None
    except (KeyError, configparser.NoSectionError):
        return None
    except:
        if default:
            return default
        else:
            print('Error with key {0} in section {1}'.format(param, section))
            sys.exit(1)

# Retriever parameters
RETRIEVER_CONNECT_TIMEOUT = float(environ.get('HTTPOBS_RETRIEVER_CONNECT_TIMEOUT') or
                                  __conf('retriever', 'connect_timeout'))
RETRIEVER_READ_TIMEOUT = float(environ.get('HTTPOBS_RETRIEVER_READ_TIMEOUT') or
                               __conf('retriever', 'read_timeout'))
RETRIEVER_USER_AGENT = environ.get('HTTPOBS_RETRIEVER_USER_AGENT') or __conf('retriever', 'user_agent')
RETRIEVER_CORS_ORIGIN = environ.get('HTTPOBS_RETRIEVER_CORS_ORIGIN') or __conf('retriever', 'cors_origin')

# Scanner configuration
SCANNER_ALLOW_LOCALHOST = (environ.get('HTTPOBS_SCANNER_ALLOW_LOCALHOST') == 'yes' or
                           __conf('scanner', 'allow_localhost', bool))
SCANNER_MOZILLA_DOMAINS = [domain.strip() for domain in (environ.get('HTTPOBS_SCANNER_MOZILLA_DOMAINS') or
                                                         __conf('scanner', 'mozilla_domains')).split(',')]
SCANNER_PINNED_DOMAINS = [domain.strip() for domain in (environ.get('HTTPOBS_SCANNER_PINNED_DOMAINS') or
                                                        __conf('scanner', 'pinned_domains')).split(',')]
