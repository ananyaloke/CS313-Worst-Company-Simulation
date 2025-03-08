"""
Student information for this assignment:

On my/our honor, Ananya Loke and Vijay Avala, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: asl3324
UT EID 2: vma736
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC): # pylint: disable=too-many-instance-attributes
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self._name = name
        self._manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary

    @abstractmethod
    def work(self):
        """Abstract Method for how employees must work"""


    def interact(self, other):
        """Simulates an interaction between this employee and another employee"""
        if other.name not in self.relationships:
            self.relationships[other.name] = 0

        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif (self.happiness >= HAPPINESS_THRESHOLD) and (other.happiness >= HAPPINESS_THRESHOLD):
            self.relationships[other.name] += 1
        else:
            self.happiness -= 1
            self.relationships[other.name] -= 1

    @property
    def name(self):
        """returns name of the employee"""
        return self._name

    #@name.setter
    #def name(self, name):
    #    self._name = name

    @property
    def manager(self):
        """returns manager of the employee"""
        return self._manager

    #@manager.setter
    #def manager(self, manager):
    #    self._manager = manager

    @property
    def performance(self):
        """returns performance of the employee"""
        return self._performance

    @performance.setter
    def performance(self, performance):
        if performance < PERCENTAGE_MIN:
            self._performance = PERCENTAGE_MIN  # Use _performance instead
        elif performance > PERCENTAGE_MAX:
            self._performance = PERCENTAGE_MAX
        else:
            self._performance = performance

    @property
    def happiness(self):
        """returns happiness of the employee"""
        return self._happiness

    @happiness.setter
    def happiness(self, happiness):
        if happiness < PERCENTAGE_MIN:
            self._happiness = PERCENTAGE_MIN
        elif happiness > PERCENTAGE_MAX:
            self._happiness = PERCENTAGE_MAX
        else:
            self._happiness = happiness

    @property
    def salary(self):
        """returns salary of the employee"""
        return self._salary

    @salary.setter
    def salary(self, salary):
        if salary >= 0:
            self._salary = salary  # Use _salary instead
        else:
            raise ValueError(SALARY_ERROR_MESSAGE)

    def daily_expense(self):
        """Simulates the employee's daily expenses"""
        self.savings -= DAILY_EXPENSE
        self.happiness -= 1

    def __str__(self):
        return (f"{self.name}\n" f"\tSalary: ${self.salary}\n" f"\tSavings: ${self.savings}\n"
                f"\tHappiness: {self.happiness}%\n" f"\tPerformance: {self.performance}%")



class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """

    def work(self):
        performance_change = random.randrange(-5, 6)
        if performance_change <= 0:
            self.happiness -= 1
            for key in self.relationships:
                self.relationships[key] -= 1
            self.performance -= 5  # Ensures performance can decrease
        else:
            self.happiness += 1
            self.performance += 5  # Ensures performance can increase

    @property
    def name(self):
        """Make name immutable to trigger AttributeError"""
        return self._name



class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """

    def work(self):
        performance_change = random.randrange(-15, 16)
        if performance_change <= 0:
            self.happiness -= 2
        else:
            self.happiness += 1
        self.performance += performance_change

    def interact(self, other):
        super().interact(other)
        if other is self.manager:
            if (other.happiness > HAPPINESS_THRESHOLD and
            self.performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD):
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary = self.salary //2
                self.happiness -= 5
                if self.salary <= 0:
                    self.is_employed = False


class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """

    def __init__(self, name, manager, salary, savings):
        super().__init__(name, manager, salary, savings)

    def work(self):
        performance_change = random.randrange(-10, 11)
        self.performance += performance_change
        
        if performance_change >= 0:
            self.happiness += 1  

    def interact(self, other):
        super().interact(other)
        
        if other == self.manager:
            if other.happiness > HAPPINESS_THRESHOLD and self.performance >= PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1 
