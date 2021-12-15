


class BaseClass:
    name = "Base"
    
    @classmethod
    def get_name(cls):
        return cls
    
    
BaseClass.get_name()