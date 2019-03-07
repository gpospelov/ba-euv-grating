import collections


class ClassParameters:
    """
    Class to accumulate all values found in class members for logging purposes.
    """
    def __init__(self, item):
        self.m_parameters = collections.OrderedDict()
        self.find_parameters(item)

    def find_parameters(self, item):
        """
        Find registered parameters in Python class
        """
        keys = item.__dict__.keys()
        keys = sorted(keys)
        for key in keys:
            var = item.__dict__[key]
            if "m_" in key and isinstance(var, (int, float)):
                self.m_parameters[key] = var

    def items(self):
        return self.m_parameters.items()


class RunParameters:
    """
    Class to save all values in all builders of the project.
    """
    def __init__(self):
        self.m_run_parameters = collections.OrderedDict()

    def add_parameters(self, item):
        if item:
            item_name = type(item).__name__
            self.m_run_parameters[item_name] = ClassParameters(item)

    def value_str(self, key, value):
        """
        Formats value so it look nicer in parameter table
        """
        if "time_spend" in key:
            return "{:.2f}".format(value)
        if "intensity" in key:
            return "{:.5g}".format(value)
        if "wavelength" in key:
            return "{:.4f}".format(value)
        return str(value)

    def parameter_string(self):
        result = str()
        for key, item_pars in self.m_run_parameters.items():
            result += "\n\n"
            result += "{}\n".format(key)
            for key, value in item_pars.items():
                vstr = self.value_str(key, value)
                result += "{0:30} : {1}\n".format(key, vstr)
        return result

    def parameter_tuple(self):
        result = []
        for key, item_pars in self.m_run_parameters.items():
            result.append((str(key), ""))
            for key, value in item_pars.items():
                vstr = self.value_str(key, value)
                result.append((str(key), vstr))

        return result