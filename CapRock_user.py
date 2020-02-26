class User():
    """
    All relevant user information to be able to calculate BAC.
    """
    def __init__(self, id_num, name, sex, weight):
        self._id = id_num
        self._name = name
        self._sex = sex
        self._weight = weight
        self._bac = 0.0
        self._current_drinks = []

    def get_id(self):
        """ Returns the ID of the user profile """
        return self._id

    def get_name(self):
        """ Returns the Name of the user profile """
        return self._name

    def change_name(self, new_name):
        """ Changes the Name of the user profile to new_name """
        self._name = new_name

    def get_sex(self):
        """ Returns the Sex of the user profile """
        return self._sex

    def change_sex(self, new_sex):
        """ Changes the sex of the user profile to new_sex """
        self._sex = new_sex

    def get_weight(self):
        """ Returns the weight of the user profile in lbs """
        return self._weight

    def change_weight(self,new_weight):
        """ Changes the sex of the user profile to new_weight """
        self._weight = new_weight

    def _calc_bac(self):
        """
        Calculates the BAC of the user based on what when each
        current drink was made. This returns the sum of all individual
        drink's BAC
        """
        # TODO
        bac_sum = 0
        return bac_sum

    def update_bac(self):
        """ Updates the BAC of the user """
        self._bac = self._calc_bac()

    def get_bac(self):
        """ Updates the BAC and returns the BAC of the user profile """
        self.update_bac()
        return self._bac()

    def 