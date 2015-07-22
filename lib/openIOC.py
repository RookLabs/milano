# Imports
from lxml import etree
from ioc import *

# client_action, returned_types, labels, supported_os
procTypes = ['ProcessItem', 'UserItem', 'PortItem', 'VolumeItem', 'EventLogItem', 'ServiceItem', 'DiskItem']


class OpenIOC(object):
  """docstring for OpenIOC"""

  def __init__(self, in_file_name, err_log):
    super(OpenIOC, self).__init__()
    self.tree = etree.parse(in_file_name)
    self.root = self.tree.getroot()
    self.seenIndicators = []
    self.seenItems = []
    self.err_log = err_log


  def parse(self):
    root = self.root

    # Grab meta data
    name = str(root.find('{http://schemas.mandiant.com/2010/ioc}short_description').text)
    doc = str(root.find('{http://schemas.mandiant.com/2010/ioc}description').text)
    defID = str(root.attrib['id'])

    # Initialize IOC
    self.ioc = IOC(name, doc, defID, self.err_log)

    indicatorDict = {}
    indicatorDict[defID] = {}
    self.indDict = indicatorDict[defID]

    self.recursiveParse( root, self.ioc.logic)

    return [self.ioc]


  def recursiveParse(self, node, outerLogic):
    isValueUsed = 0

    # Iterate Indicators and recurse
    for indicator in node.iter('{http://schemas.mandiant.com/2010/ioc}Indicator'):
      # Make sure we don't do extra recursion
      if indicator.attrib['id'] not in self.seenIndicators:
        self.seenIndicators.append(indicator.attrib['id'])
      
        # IndicatorItems
        outerLogic[indicator.attrib['operator']] = [{}]
        logic = outerLogic[indicator.attrib['operator']]
        # Create recursion logic i.e.
        self.recursiveParse(indicator, logic[0])

        # Iterate IndicatorItems
        for item in indicator.iter('{http://schemas.mandiant.com/2010/ioc}IndicatorItem'):
          # Make sure we haven't added this from a subgroup
          if item.attrib['id'] not in self.seenItems:
            self.seenItems.append(item.attrib['id'])

            # Contexts / Contents
            for child in item.getchildren():
              # Context
              if 'document' in child.attrib.keys():
                type_name = str(child.attrib['document'])
                search = str(child.attrib['search'])

                # Check for key_value_pairs
                if type_name == 'RegistryItem':
                  # REGISTRY_KEY
                  if search == 'RegistryItem/Path':
                    type_name = 'REGISTRY_KEY'
                    nextChild = item.getnext().getchildren()[1]
                    if item.getnext().getchildren()[0].attrib['search'] == 'RegistryItem/Text':
                      isValueUsed = 1
                      self.ioc.key_value_pairs.append({ 'key': value, 'value': nextChild.text })
                  # REGISTRY_VALUE
                  elif search == 'RegistryItem/Text':
                    type_name = 'REGISTRY_VALUE'
                    if not isValueUsed:
                      self.err_log.write('\nERROR: REGISTRY_KEY without REGISTRY_VALUE.\n')
                      continue
                    else:
                      isValueUsed = 0
                      continue
                  # ???
                  else:
                    self.err_log.write('\nERROR: Unknown issue with RegistryItem. 1\n')
                    continue
              
              # Content --> store data
              elif 'type' in child.attrib.keys():
                value = str(child.text)

                # If this artifact uses another GRR artifact
                if type_name in procTypes:
                  data = value

                elif type_name in ['RegistryItem', 'REGISTRY_KEY', 'REGISTRY_VALUE']:
                  data = value

                elif type_name in ['FileItem', 'DriverItem', 'HookItem']:
                  if type_name == 'FileItem':
                    prev_search = child.getprevious().attrib['search'][9:]
                    if prev_search == 'FullPath':
                      self.ioc.isUnix = 1
                    elif prev_search in self.ioc.dump.keys():
                      # TODO: Handle dump
                      continue
                    
                  type_name = 'FILE'
                  if value in ['true','false']:
                    continue

                  # Check if isWindows or isUnix
                  if '\\' in value or 'exe' in value:
                    self.ioc.isWindows = 1
                  elif '/':
                    self.ioc.isUnix = 1
                  # Set OS support
                  self.ioc.setSupportedOS()
                  data = value

                elif type_name == 'DriverItem':
                  # ???? Not sure what to do with this yet... ????
                  data = value
                else:
                  continue

              # Block to append properly
                # If ARTIFACT_FILE
                if type_name in procTypes:
                  # If no ARTIFACT_FILES yet, create dict
                  if 'ARTIFACT_FILES' not in self.indDict.keys():
                    self.indDict['ARTIFACT_FILES'] = {}
                  # If none of this type yet, create list
                  if type_name not in self.indDict['ARTIFACT_FILES'].keys():
                    self.indDict['ARTIFACT_FILES'][type_name] = []

                  # Append the observable to self.indDict
                  self.indDict['ARTIFACT_FILES'][type_name].append(data)
                  logic.append(data)
                # NOT an ARTIFACT_FILE
                else:
                  # If none of this type yet, create list
                  if type_name not in self.indDict.keys():
                    self.indDict[type_name] = []

                  # Append the observable to indDict
                  self.indDict[type_name].append(data)
                  logic.append(data)



