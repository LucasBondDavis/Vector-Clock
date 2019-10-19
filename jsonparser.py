import json
'''
How to use this class:
open the json file to read, and pass it to jsonparser's constructor as opened_file
call get_dict() to get a diction with site_id as keys and site info as values.
site info is also a dictionary with entries like 'ip_address' as key, and int or string as values.
'''
class jsonparser(object):
    def __init__(self, opened_file):
        self.reader = opened_file
        self.number_of_sites = -1
    def get_dict(self):
        j_dict = json.load(self.reader)
        site_dict = j_dict['hosts'] # site_dict is a dictionary with keys as site id, value as a another dictionary with information
        self.number_of_sites = len(site_dict)
        return site_dict
    # REMARK: get_number_of_sites can only be called after calling get_dict() successfully.
    def get_number_of_sites(self):
        return self.number_of_sites

if __name__ == '__main__':
    f = open('bin/knownhosts.json', 'r')
    '''
    jdict = json.load(f)
    print(jdict)
    print(jdict['hosts'])
    
    siteDict = jdict['hosts']
    print(siteDict['alpha'])
    '''
    j_parser = jsonparser(f)
    siteDict = j_parser.get_dict()
    for site_id in siteDict:
        print (site_id)
        for entry in siteDict[site_id]:
            print('\t' + entry + ' :' + str(siteDict[site_id][entry]) )
    print( j_parser.get_number_of_sites() )
    
    
    f.close()