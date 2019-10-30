import pandas as pd
from interfaces.ttypes import ElementConfiguration, ElementType, ElementState


class ElementTable:
    def __init__(self):
        self.elements_table = pd.DataFrame()

    def insert(self, element_id, element_type, element_ip='unavailable', element_port=0,
               element_state=ElementState.WAITING):
        new_row = pd.DataFrame([{'type': element_type, 'ip': element_ip,
                                 'port': element_port, 'state': element_state}], index=[element_id])
        self.elements_table = self.elements_table.append(new_row)

    def get_servers_configuration(self):
        filter_configuration = self.elements_table[self.elements_table['type'] != ElementType.CLIENT]
        elements_configurations = []
        for element in filter_configuration.itertuples(index=False):
            elements_configurations += [ElementConfiguration(type=getattr(element, 'type'),
                                                             ip=getattr(element, 'ip'),
                                                             port=getattr(element, 'port'))]
        return elements_configurations

    def get_complete_configuration(self):
        elements_configurations = []
        for element in self.elements_table.itertuples(index=False):
            elements_configurations += [ElementConfiguration(id=element.index,
                                                             type=getattr(element, 'type'),
                                                             ip=getattr(element, 'ip'),
                                                             port=getattr(element, 'port'))]
        return elements_configurations

    def get_element_state(self, element_id):
        return self.elements_table.loc[[element_id], ['state']].values[0].item()

    def get_element_type(self, element_id):
        return self.elements_table.loc[[element_id], ['type']].values[0].item()

    def set_element_state(self, element_id, state):
        self.elements_table.at[element_id, 'state'] = state
        return self.get_element_state(element_id)

    def exist_type_in_state(self, element_type: ElementType, element_state: ElementState):
        if element_state in self.elements_table[self.elements_table['type'] == element_type].values:
            return True
        else:
            return False

    def update_state_by_type(self, element_type: ElementType, state: ElementState):
        self.elements_table.loc[self.elements_table['type'] == element_type, 'state'] = state

