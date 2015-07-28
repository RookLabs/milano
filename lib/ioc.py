# Imports


class IOC(object):
  """docstring for IOC"""

  def __init__(self, name, doc, defID):
    super(IOC, self).__init__()
    self.name = name
    self.doc = doc
    self.id = defID
    self.isWindows = 0
    self.isUnix = 0
    self.key_value_pairs = []
    # { type: [values] }  OR  { type: [subtype: [values]] }
    self.indDict = {
      'md5': []
    }
    # { operator: [ values, { operator: [...] } ] }
    self.logic = {}
    # { type: [values] }
    self.dump = {}


  def add(self, key, value):
    # TODO: Error on value true/false
    if not value:
      return

    # Check if isWindows or isUnix
    if '\\' in value['value'] or 'exe' in value['value']:
      self.isWindows = 1
    elif '/':
      self.isUnix = 1
    # Set OS support
    self.setSupportedOS()
    
    if key in self.indDict.keys():
      self.indDict[key].append(value)
    elif 'ARTIFACT_FILES' in self.indDict.keys()\
      and key in self.indDict['ARTIFACT_FILES'].keys():

      self.indDict['ARTIFACT_FILES'][key].append(value)
    else:
      if key not in self.dump.keys():
        self.dump[key] = []
      self.dump[key].append(value)


  # Set the supported_os attribute based on flags
  def setSupportedOS(self):
    full_os_list = ['Windows', 'Linux', 'Darwin']
    
    # This IOC is almost done, determine supported_os
    if self.isWindows:
      self.supported_os = '['+full_os_list[0]+']'
    elif self.isUnix:
      self.supported_os = str(full_os_list[1:])
    else:
      self.supported_os = str(full_os_list)


  def findValueByID(self, refid):
    for key in self.indDict.keys():
      if self.indDict[key]['id'] == refid:
        return self.indDict[key]['value']
