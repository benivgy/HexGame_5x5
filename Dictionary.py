import json
class Dict():

    def __init__(self, path):
        self.path = path #String of the path from the content root
        self.dic = json.load(open(self.path)) #A python dictionary


    def getDic(self):
        # Open and read the JSON file
        with open(self.path, 'r') as json_file:
            # Load JSON from the file into a dictionary
            json_dict = json.load(json_file)

        return json_dict

    def dumpDic(self,dictionary):
        #Export the given dictionary as JSON file (overwrite)
        with open(self.path, 'w')as json_file:
            json.dump(dictionary, json_file)