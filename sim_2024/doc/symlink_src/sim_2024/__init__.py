class package_warning(UserWarning):
    """package warning
    
    """
    pass

class GeneratorError(Exception):
    """exception raised when a generator raise a null state
    
    """
    def __init__(self):
        self.add_note('random generator raise a null state')
