#! /bin/env python3
from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """观察者的基类"""
    @abstractmethod
    def update(self, observable, object):
        pass


class Observable:
    """被观察者的基类"""
    def __init__(self):
        self._observers = []

    def addObserver(self, observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        self._observers.remove(observer)

    def notifyObservers(self, object=0):
        for o in self._observers:
            o.update(self, object)


class WaterHeater(Observable):
    """热水器"""
    def __init__(self):
        super().__init__()
        self._temperature = 25

    def getTemperature(self):
        return self._temperature

    def setTemperature(self, tempterature):
        self._temperature = tempterature
        print('Current temperature is: ' + str(self._temperature) + ' ℃')
        self.notifyObservers()


class WashingMode(Observer):
    def update(self, observable, object):
        if isinstance(observable, WaterHeater) and observable.getTemperature(
        ) >= 50 and observable.getTemperature() < 70:
            print('time for washing')


class DrinkingMode(Observer):
    def update(self, observable, object):
        if isinstance(observable,
                      WaterHeater) and observable.getTemperature() >= 100:
            print('time for drinking')


if __name__ == '__main__':
    heater = WaterHeater()
    washing = WashingMode()
    drinking = DrinkingMode()
    heater.addObserver(washing)
    heater.addObserver(drinking)
    heater.setTemperature(60)
    heater.setTemperature(100)
