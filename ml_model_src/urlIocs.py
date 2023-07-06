from typing import List, Dict
import json
import re

class IoCItem:          # original IoC item     
    ioc_string: str     # original IoC string  
    ioc_type: str       # IoC type
    # ioc_location: Tuple[int, int]  # original

    def __init__(self, ioc_string, ioc_type):
        
        self.ioc_string = ioc_string
        self.ioc_type = ioc_type

    def __list__(self):
        return [self.ioc_type,self.ioc_string]
        




class IoCIdentifier:

    # IoC pattern stored in json file: "./ioc_regexPattern.json" and "./ioc_replaceWord.json"
    # https://github.com/PaloAltoNetworks/ioc-parser/blob/master/patterns.ini
    ioc_regexPattern = {}
    ioc_replaceWord = {}

    report_text: str
    ioc_list: List[IoCItem]

    deleted_character_count: int
    replaced_text: str
    replaced_ioc_list: List[IoCItem]
    replaced_ioc_dict: Dict[int, str]

    def __init__(self, text: str = None):
        self.ioc_list = []

        self.replaced_text = ""
        self.replaced_ioc_list = []
        self.replaced_ioc_dict = {}
        self.deleted_character_count = 0

        self.load_ioc_pattern()
        self.report_text = text

    def load_ioc_pattern(self, ioc_regexPattern_path: str = "./ml_model_src/ioc_regexPattern.json"):
        with open(ioc_regexPattern_path) as pattern_file:
            self.ioc_regexPattern = json.load(pattern_file)
        

    
    def ioc_identify(self, text: str = None):
        # logging.info("---ioc protection: Identify IoC items with regex in cti text!---")
        self.report_text = text if text is not None else self.report_text

        # Find all IoC item in the text
        for ioc_type, regex_list in self.ioc_regexPattern.items():
            for regex in regex_list:
                matchs = re.finditer(regex, self.report_text)
                for m in matchs:
                    ioc_item = IoCItem(m.group(), ioc_type).__list__()
                    print("IOC: ---> ", ioc_item)
                    self.ioc_list.append(ioc_item)

        # self.ioc_overlap_remove()
        if len(self.ioc_list) == 0:
            return
    
    
    
    


def preprocess_file(report_file: str) -> str:
    
    file_path, extension = os.path.splitext(report_file)

    if extension == ".txt":
        report_text = read_txt(report_file)
    elif extension == ".html":
        report_text = read_html(report_file)
    elif extension == ".pdf":
        report_text = read_pdf(report_file)
    else:
        raise Exception(f"Unknown report file type: {extension} in {report_file}!")

    cleared_text = clear_text(report_text)
    
    return cleared_text
