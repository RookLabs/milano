# Imports
from xml.etree import ElementTree
from ioc import *

# client_action, returned_types, labels, supported_os
procTypes = ['ProcessItem', 'UserItem', 'PortItem', 'VolumeItem', 'EventLogItem', 'ServiceItem', 'DiskItem']

Filename,Category,Reference,SHA1,MD5,SHA256 = (0,1,2,3,4,5)

class OpenIOC(object):
  """docstring for OpenIOC"""

  def __init__(self, in_file_name):
    super(OpenIOC, self).__init__()
    self.in_file_name = in_file_name
    self.tree = ElementTree.parse(in_file_name)
    self.root = self.tree.getroot()
    self.seenIndicators = []
    self.seenItems = []
    self.seenRegItems = []
    self.data = []


  def parse(self):
    root = self.root

    # Grab meta data
    name = str(root.getchildren()[0].find('{http://openioc.org/schemas/OpenIOC_1.1}short_description').text)
    doc = str(root.getchildren()[0].find('{http://openioc.org/schemas/OpenIOC_1.1}description').text)
    defID = str(root.attrib['id'])

    # Initialize IOC
    self.ioc = IOC(name, doc, defID)

    # Recursive through Indicators
    self.recursiveParse( root, self.ioc.logic )

    self.defaultReturnData()

    # Get the associated data and fill up self.data
    self.parseParameters( root )

    return self.data


  def recursiveParse(self, node, outerLogic):
    # Iterate Indicators and recurse
    for indicator in node.iter('{http://openioc.org/schemas/OpenIOC_1.1}Indicator'):
      # Make sure we don't do extra recursion
      if indicator.attrib['id'] not in self.seenIndicators:
        self.seenIndicators.append(indicator.attrib['id'])
      
        # IndicatorItems
        outerLogic[indicator.attrib['operator']] = [{}]
        logic = outerLogic[indicator.attrib['operator']]
        # Create recursion logic i.e.
        self.recursiveParse(indicator, logic[0])

        # Iterate IndicatorItems
        for item in indicator.iter('{http://openioc.org/schemas/OpenIOC_1.1}IndicatorItem'):
          item_id = item.attrib['id']
          # Make sure we haven't added this from a subgroup
          if item_id not in self.seenItems:
            self.seenItems.append(item_id)

            # Contexts / Contents
            for child in item.getchildren():
              # Context
              if 'document' in child.attrib.keys():
                type_name = str(child.attrib['document'])
                search = str(child.attrib['search'])

                # Find key_value_pairs AND registry values w/o key
                if type_name == 'RegistryItem':
                  # REGISTRY_KEY
                  if search == 'RegistryItem/Path':
                    type_name = 'REGISTRY_KEY'
                    if self.isKeyValuePair(item):
                      continue
                  # REGISTRY_VALUE
                  elif search == 'RegistryItem/Text':
                    type_name = 'REGISTRY_VALUE'
                    # if str(child.getnext().text) not in self.seenRegItems:
                      # self.err_log.write('\nERROR: REGISTRY_KEY without REGISTRY_VALUE.\n')
                    continue
              
              # Content --> store value
              elif 'type' in child.attrib.keys():
                value = str(child.text)

                if value not in self.seenRegItems:
                  # Append the observable to ioc.indDict
                  self.ioc.add(str(child.attrib['type']), { 'id': item_id, 'value': value })
                  logic.append(value)


  def isKeyValuePair(self, item):
    nextChild_Context = item.getnext().getchildren()[0]
    nextChild_Content = item.getnext().getchildren()[1]

    if nextChild_Context.attrib['search'] == 'RegistryItem/Text':
      key = str(item.getchildren()[1].text)
      value = str(nextChild_Content.text)

      self.seenRegItems.append(key)
      self.seenRegItems.append(value)
      self.ioc.key_value_pairs.append({ 'key': key, 'value': value })

      return True


  def parseParameters(self, root):
    # If no params, catch exception and leave the default self.data
    try:
      param = root.getchildren()[2].getchildren()[0]
    except:
      return

    # Wipe out the default
    self.data = []
    
    # Iterate <parameters> sections (should be 1)
    for item in root.iter('{http://openioc.org/schemas/OpenIOC_1.1}parameters'):
      # Iterate <param> items
      for param in item.iter('{http://openioc.org/schemas/OpenIOC_1.1}param'):
        value_node = param.getchildren()[0]
        value_list = value_node.text.split(',')

        value_list_noQuotes = []

        for value in value_list:
          value_list_noQuotes.append(value.replace("'",""))

        # Keep reference of which IOC file this came from
        value_list_noQuotes.append(self.in_file_name)
        # Append this row to self.data
        self.data.append(value_list_noQuotes)


  def defaultReturnData(self):
    for item in self.ioc.indDict['md5']:
      self.data.append( ['','','','',item['value'],'',self.in_file_name] )





