from requests.exceptions import RequestException

class MutualAuthenticationError(RequestException): ...
class SPNEGOExchangeError(RequestException): ...

KerberosExchangeError = SPNEGOExchangeError