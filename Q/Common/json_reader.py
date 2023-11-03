import json
import sys
import map as m

class jsonReader():

    def __init__(self, input):
        self.input = input
    
    def getJson(self) -> list:
        try:
            # Read JSON input from STDIN
            json_list = []

            for json_obj in self.input:
                json_dict = json.loads(json_obj)
                json_list.append(json_dict)
            # Get the map and tile placements from the input JSON
            return json_list

        except Exception as e:
            # Handle exceptions if necessary
            print("Error:", str(e))
            
    