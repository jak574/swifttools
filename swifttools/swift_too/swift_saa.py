from .swift_clock import TOOAPI_ClockCorrect
from .common import TOOAPI_Baseclass, TOOAPI_Daterange, swiftdatetime
from .too_status import Swift_TOO_Status


class Swift_SAA_Entry(TOOAPI_Baseclass, TOOAPI_ClockCorrect):
    """Simple class describing the start and end time of a Swift SAA passage.
     Attributes
    ----------
    begin : datetime
        Start time of the SAA passage
    end : datetime
        End time of the SAA passages
    """

    # API details
    api_name = "Swift_SAA_Entry"
    # Returned values
    _attributes = ["begin", "end"]
    # Display names of columns
    _varnames = {"begin": "Begin", "end": "End"}

    def __init__(self):
        # Attributes
        self.begin = None
        self.end = None
        # Internal values
        self._isutc = True

    def __header_title(self, parameter):
        title = self._varnames[parameter]
        value = getattr(self, parameter)
        if type(value) == swiftdatetime:
            if value.isutc:
                title += " (UTC)"
            else:
                title += " (Swift)"
        return title

    @property
    def _table(self):
        header = [self.__header_title("begin"), self.__header_title("end")]
        data = [[self.begin, self.end]]
        return header, data

    @property
    def table(self):
        return ["begin", "end"], [[self.begin, self.end]]


class Swift_SAA(TOOAPI_Baseclass, TOOAPI_Daterange, TOOAPI_ClockCorrect):
    """Class to obtain Swift SAA passage times. Two versions are available: The
    Spacecraft definition (default) or an estimate of when the BAT SAA flag is
    up. Note that the BAT SAA flag is dynamically set based on count rate, so
    this result only returns an estimate based on when that is likely to happen.

    Attributes
    ----------
    begin : datetime
        Start of the period for which to fetch SAA passages
    end : datetime
        End of the period for which to fetch SAA passages
    bat : boolean
        If set to `True`, use BAT calculation for SAA passages, otherwise, use
        spacecraft.
    entries : list
        Array of Swift_SAA_Entry classes containing the windows.
    status : Swift_TOO_Status
        Status of API request
    username : str (default 'anonymous')
        TOO API username.
    """

    # API details
    api_name = "Swift_SAA"
    # Arguments
    _parameters = ["username", "begin", "end", "bat"]
    # Returned Values
    _attributes = ["entries", "status"]
    # Returned classes
    _subclasses = [Swift_SAA_Entry, Swift_TOO_Status]
    # Local parameters
    _local = ["shared_secret", "length"]

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        begin : datetime
            Start of the period for which to fetch SAA passages
        end : datetime (optional)
            End of the period for which to fetch SAA passages
        length : int (default: 1)
            Number of days to calculate for
        bat : boolean
            If set to `True`, use BAT calculation for SAA passages, otherwise, use
            spacecraft.
        username : str (default 'anonymous')
            TOO API username.
        shared_secret : str (default 'anonymous')
            TOO API shared secret
        """
        # Attributes
        self.begin = None
        self.end = None
        self.length = 1
        self.bat = False
        # parse arguments
        self._parseargs(*args, **kwargs)
        self.status = Swift_TOO_Status()
        # Returned values
        self.entries = None
        # Internal values
        self._isutc = True

        # Submit if enough parameters are passed to the constructor
        if self.validate():
            self.submit()
        else:
            self.status.clear()

    def __getitem__(self, index):
        return self.entries[index]

    def __len__(self):
        return len(self.entries)

    @property
    def _table(self):
        if self.entries is None:
            return [], []
        else:
            vals = list()
            for i in range(len(self.entries)):
                header, values = self.entries[i]._table
                vals.append([i] + values[0])
            return ['#'] + header, vals

    def validate(self):
        """Simple validation for submit"""
        if self.begin is not None and self.end is not None:
            return True
        return False


SAA = Swift_SAA
