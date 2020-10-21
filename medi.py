import sys, getopt
import json


def get_children(d, all=False):
    """Iteratively finds nestd elements from dictionary <d>
    Args:
        d (dict): dictionary of nested elements
    
    Kwargs:
        all (bool): if True, gets whole tree, if False, returns first sub level
    
    Returns:
        list: flat list of elements discovered.
    """
    names = []
    if 'children' in d.keys():
        names.extend([every['name'] for every in d['children']])
        if all:
            for each in d['children']:
                names.extend(get_children(each))        
    return names


def flatten(l):
    for el in l:
        if '__iter__' in dir(el) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


class MEDI:

    def __init__(self, yr):
        """Class for mapping MEDI sessions. Takes one argument,
        a year string: YYYY
        """
        self.year = str(yr)
        self.courses = ['Foundations', 'Cardio', 'Respiratory', 'Renal', 'Neuro', 'Msk', 'DNM', 'EndoRepro', 'HemeOnc', 'InI', 'MultiSys']
        self.allTags = []
        self.allTypes = ['Tour', 'Experiment', 'ComputerSimulation', 'Technique', 'Demonstration', 'Challenge', 'Other']
        self.allAssignmentTypes = ['ProblemSet', 'Presentation', 'Report', 'Reflection', 'Quiz']
        self.allGroupedBy = ['degree', 'C', 'Python', 'Matlab', 'R', 'self']
        self.allResources = {'university':['software', 'computerLab', 'researchLab', 'room', 'equipment', 'graduateStudent', 'professor', 'staff', 'other'], 
                             'student':['computer', 'phone', 'tablet', 'other'], 
                             'custom':['equipment', 'software', 'consumables', 'staff', 'faculty']}
        self.allTrainingType = ['CITI', 'LabSafety', 'BioSafety', 'ChemSafety', 'LaserSafety', 'RadiationSafety', 'HazardousMaterialsTransport', 'NonLabPersonnelSafety', 'IRB', 'ResearchConsent', 'Other']
    
        self.course = ''
        self.week = 0
        self.dates = []
        self.title = ''
        self.objectives = []
        self.type = []
        self.assignment = True
        self.assignmentType = []
        self.tags = []
        self.resources = []
        self.grouped = False
        self.groupedBy = []
        self.groupSize = 32
        self.numSessions = 1
        self.preReading = False
        self.training = False
        self.trainingType = []
        self.SETS = []
        
        self._get_tags(f'curriculumMap{self.year}.json')
        
    def show(self, option=None):
        if not option:
            print(f'MEDI class attributes include: {sorted(list(self.__dict__.keys()))}')
            return
        if not isinstance(option, (str, bytearray, )):
            raise TypeError(f'Inappropriate argument type for method, show: need string or bytearray, got {type(option)}')
            return
        elif isinstance(option, bytearray):
            option = option.decode('utf-8')
        try:
            print(self.__getattribute__(option))
        except AttributeError:
            print(f'MEDI class does not have attribute: {option}. Attributes include {sorted(list(self.__dict__.keys()))}')
            return 
        return list(self.__getattribute__(option))
    
    def _get_tags(self, fname):
        with open(fname, 'r') as jdata:
            jstr = jdata.read()
            jdict = json.loads(jstr)
            jdict = jdict['children']  # level 1
        lvl2 = []
        lvl3 = []
                        
        for each in jdict:
            lvl2.append(each)
        lvl2 = sorted(lvl2, key = lambda i: i['name'])
        for each in lvl2:
            lvl3.extend(get_children(each))
            
        self.allTags = ([i['name'] for i in lvl2], lvl3)