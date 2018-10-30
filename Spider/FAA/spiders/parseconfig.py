import configparser


class Parsedeparture(object):
    def __init__(self):
        self.config = {}
        self.cfg = configparser.ConfigParser()
        self.cfg.read("./FAA/spiders/spiderconfig.ini", encoding="utf-8")
        if 'Departure' not in self.cfg.sections():
            print('[!] Failed to find configuration of Departure')
            raise ValueError

    def readstatistics(self):
        if 'statistics' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'statistics\' in Departure')
            raise ValueError
        self.config['statistics'] = self.cfg['Departure']['statistics']
        self.config['statistics'] = self.config['statistics'].split(',')
        self.config['statistics'] = list(map(str.strip, self.config['statistics']))
        self.config['statistics'] = list(map(str.capitalize, self.config['statistics']))

    def readairports(self):
        if 'origin_airports' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'origin_airports\' in Departure')
            raise ValueError
        self.config['origin_airports'] = self.cfg['Departure']['origin_airports']
        self.config['origin_airports'] = self.config['origin_airports'].split(',')
        self.config['origin_airports'] = list(map(str.strip, self.config['origin_airports']))
        self.config['origin_airports'] = list(map(str.upper, self.config['origin_airports']))

    def readairlines(self):
        if 'airlines' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'airlines\' in Departure')
            raise ValueError
        self.config['airlines'] = self.cfg['Departure']['airlines']
        self.config['airlines'] = self.config['airlines'].split(',')
        self.config['airlines'] = list(map(str.strip, self.config['airlines']))
        self.config['airlines'] = list(map(str.upper, self.config['airlines']))

    def readmonths(self):
        if 'months' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'months\' in Departure')
            raise ValueError
        self.config['months'] = self.cfg['Departure']['months']
        self.config['months'] = self.config['months'].split(',')
        self.config['months'] = list(map(str.strip, self.config['months']))
        self.config['months'] = list(map(str.upper, self.config['months']))

    def readdays(self):
        if 'days' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'days\' in Departure')
            raise ValueError
        self.config['days'] = self.cfg['Departure']['days']
        self.config['days'] = self.config['days'].split(',')
        self.config['days'] = list(map(str.strip, self.config['days']))
        self.config['days'] = list(map(str.upper, self.config['days']))

    def readyears(self):
        if 'years' not in self.cfg['Departure']:
            print('[!] Read Config: Failed to find \'years\' in Departure')
            raise ValueError
        self.config['years'] = self.cfg['Departure']['years']
        self.config['years'] = self.config['years'].split(',')
        # self.config['days'] = list(map(str.capitalize(), self.config['days']))
        # self.config['days'] = list(map(str.strip, self.config['days']))

    def readall(self):
        self.readstatistics()
        self.readairports()
        self.readairlines()
        self.readmonths()
        self.readdays()
        self.readyears()
        return self.config
