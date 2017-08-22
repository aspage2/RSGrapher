class SampleState:
    DFA = {"INFO": {"N": "DATA", "I": "INFO"},
           "DATA": {"N": "TEST", "I": "INFO_DATA"},
           "TEST": {"N": "ELASTIC", "D":"DATA", "I":"INFO_TEST", "T":"TEST"},
           "ELASTIC": {"N": "FINAL", "D": "DATA", "I":"INFO_ELASTIC", "T":"TEST", "E":"ELASTIC"},
           "FINAL": {"N": "END", "I":"INFO_FINAL","T":"TEST", "E":"ELASTIC", "D":"DATA"},
           "END":{},
           "INFO_DATA":{"N":"DATA", "D":"DATA"},
           "INFO_TEST":{"N":"DATA", "D":"DATA", "T":"TEST"},
           "INFO_ELASTIC":{"N":"DATA", "D":"DATA", "T": "TEST", "E":"ELASTIC"},
           "INFO_FINAL":{"N":"DATA", "D":"DATA", "T": "TEST", "E":"ELASTIC", "F":"FINAL"}}

    def __init__(self, listener):
        self.state = None
        self.listener = listener

    def set_state(self, state):
        if state not in SampleState.DFA:
            raise ValueError()
        self.state = state
        self.listener.set_state(state)

    def next(self, char):
        if self.state is None:
            self.state = "INFO"
        else:
            if char not in SampleState.DFA[self.state]:
                return
            self.state = SampleState.DFA[self.state][char]
        self.listener.set_state(self.state)
