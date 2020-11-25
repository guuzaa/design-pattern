from abc import ABCMeta, abstractmethod


class Context(metaclass=ABCMeta):
    def __init__(self):
        self._states = []
        self._curState = None
        self._stateInfo = 0

    def addState(self, state):
        if (state not in self._states):
            self._states.append(state)

    def changeState(self, state):
        if (state is None):
            return False

        if (self._curState is None):
            print('Initialization: {}'.format(state.getName()))
        else:
            print('from {} to {}'.format(self._curState.getName(), state.getName()))

        self._curState = state
        self.addState(state)

        return True

    def getState(self):
        return self._curState

    def _setStateInfo(self, stateInfo):
        self._stateInfo = stateInfo
        for state in self._states:
            if (state.isMatch(stateInfo)):
                self.changeState(state)

    def _getStateInfo(self):
        return self._stateInfo


class State:
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def isMatch(self, stateInfo):
        return False

    @abstractmethod
    def behavior(self, context):
        pass


# ------------------------------------------------------------ #
#                   Implement Class                             #
# ------------------------------------------------------------ #


class Water(Context):
    def __init__(self):
        super().__init__()
        self.addState(SolidState('Solid'))
        self.addState(LiquidState('Liquid'))
        self.addState(GaseousState('Gaseous'))
        self.setTemperature(25)

    def getTemperature(self):
        return self._getStateInfo()

    def setTemperature(self, temperature):
        self._setStateInfo(temperature)

    def riseTemperature(self, step):
        self.setTemperature(self.getTemperature() + step)

    def reduceTemperature(self, step):
        self.setTemperature(self.getTemperature() - step)

    def behavior(self):
        state = self.getState()
        if (isinstance(state, State)):
            state.behavior(self)


def singleton(cls, *args, **kwargs):
    instance = {}

    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton


@singleton
class SolidState(State):
    def __init__(self, name):
        super().__init__(name)

    def isMatch(self, stateInfo):
        return stateInfo < 0

    def behavior(self, context):
        print('Solid Temperature:', context._getStateInfo())


@singleton
class LiquidState(State):
    def __init__(self, name):
        super().__init__(name)

    def isMatch(self, stateInfo):
        return (stateInfo >= 0 and stateInfo < 100)

    def behavior(self, context):
        print('Liquid Temperature:', context._getStateInfo())


@singleton
class GaseousState(State):
    def __init__(self, name):
        super().__init__(name)

    def isMatch(self, stateInfo):
        return stateInfo >= 100

    def behavior(self, context):
        print('Gaseous Temperature:', context._getStateInfo())


if __name__ == '__main__':
    water = Water()
    water.behavior()

    water.setTemperature(-10)
    water.behavior()

    water.riseTemperature(30)
    water.behavior()

    water.riseTemperature(80)
    water.behavior()
