##parse_map

import json
import re
import cPickle

CONNECTIONS='connections'
POINTS='points' #formats definition
class map(object):
    def __init__(self,filename=None,string=None,mode=None,format=None):
        self.map = {}
        if filename and string:
            raise Exception('supply a filename or a string, not both')
        if filename:
            if mode == 'pickle' or (filename.endswith('.pickle') and not mode):
                self.load_pickle_file(filename)
            elif mode == 'json' or (filename.endswith('.json') and not mode):
                self.load_json_file(filename,format)
            else:
                raise Exception('Not sure how to parse file')
        elif string:
            if mode=='pickle':
                self.load_pickle_data(string)
            elif mode=='json':
                self.load_json_data(filename,format)
            else:
                raise Exception('Not sure how to parse string')
                
    def save(self,filename=None,mode=None):
        if filename:
            if mode=='pickle' or (filename.endswith('.pickle') and not mode):
                self.save_pickle_file(filename)
            if mode=='json' or (filename.endswith('.json') and not mode):
                self.save_json_file(filename)
            else:
                raise Exception('Not sure how to parse file')
        else:
            if mode=='pickle':
                return self.return_pickle_data()
            elif mode=='json':
                return self.return_json_data()
            else:
                raise Exception('Not sure how to parse file')
                
    def flush(self):
        self.map={}
            
    #loading functions
    
    def load_json_file(self, filename, format=None):
        f = open(filename)
        data = f.read()
        f.close()
        self.load_json_data(data,format)
        
    def load_json_data(self, data, format=None):
        jsondata = json.loads(data)
        map = python_parser().parse(jsondata)
        if format==CONNECTIONS:
            self.map = self.parse_connections(map)
        else:
            self.map = map
    
    def load_pickle_file(self, filename):
        f = open(filename,'r')
        data = f.write()
        f.close()
        self.load_pickle_data(self, data)
        
    def load_pickle_data(self, data):
        self.map = cPickle.loads(data)
        
    #saving functions
            
    def save_json_file(self, filename):
        f = open(filename,'w')
        f.write(self.return_json_data())
        f.close()
        
    def return_json_data(self):
        return json.dumps(self.map)
        
    def save_pickle_file(self, filename):
        f = open(filename,'w')
        f.write(return_pickle_data(),f)
        f.close()
        
    def return_pickle_data(self):
        return cPickle.dumps(self.map)
        
    #parsing functions
    
    def parse_connections(self, map):
        original = map['connections']
        connections = original['taxi']+original['metro']+original['bus']
        points = {}
        for connection in connections:
            points[connection[0]] = {'taxi':[],'bus':[],'metro':[]}
            points[connection[1]] = {'taxi':[],'bus':[],'metro':[]}
        for connection in original['taxi']:
            points[connection[0]]['taxi'].append(connection[1])
            points[connection[1]]['taxi'].append(connection[0])
        for connection in original['bus']:
            points[connection[0]]['bus'].append(connection[1])
            points[connection[1]]['bus'].append(connection[0])
        for connection in original['metro']:
            points[connection[0]]['metro'].append(connection[1])
            points[connection[1]]['metro'].append(connection[0])
        return points
        
    #pseudodict implementation details
    
    def __getitem__(self, name):
        return self.map[name]
        
    def __len__(self):
        return len(self.map)
        
    def __contains__(self, item):
        return item in self.map
        
    def __iter__(self):
        return self.map.__iter__()
        
        
def parse_json(data):
    return python_parser().parse(json.loads(data))

class python_parser(object):    
    def parse(self, string):
        return self.choose_parser(string)
        
    def parse_list(self, list):
        return [self.choose_parser(item) for item in list]
        
    def parse_string(self, string):
        return int(string) if re.search('^[0-9]+$',string) else str(string)
        
    def parse_dict(self, dictionary):
        result = {}
        for item in dictionary:
            result[self.parse_string(item)]=self.choose_parser(dictionary[item])
        return result

    def choose_parser(self, something):
        return (self.parse_dict(something) if isinstance(something,dict) else
                self.parse_list(something) if isinstance(something,list) else
                self.parse_string(something) if isinstance(something,unicode) or isinstance(something,str) else
                something)