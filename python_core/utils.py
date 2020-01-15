

def get_name_root(string_name):
    '''
    Trims off hierarchy and namespaces.
    '''
    return string_name.split(':')[-1]

