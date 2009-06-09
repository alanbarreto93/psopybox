'''
Particle Swarm Optimization - PyPSO 

Copyright (c) 2009 Marcel Pinheiro Caraciolo
caraciol@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

0.10 2009-04-16 Initial version.
0.20 2009-05-21 Added support for Local Topology implementation (Added StoreBestParticle method).
0.21 2009-05-24 Added support for Linux interaction.
0.22 2009-05-25 Added support for report files generation (Uses ReportAdapters).
0.23 2009-06-08 Fixed some bugs related to the INERTIA factor.
'''

"""     This module contains the PSO Engine, the PSO class is responsible
        for all the evolutionary process. It contains the PSO Algorithm related
        functions, like the Termination Criteria functions for convergence analysis, and
        the topology base class used to do the particle communication.
"""

import Consts
import random
from time import time
import Util
from sys import exit as sys_exit
from sys import platform as sys_platform

import code
import pypso



if sys_platform[:3] == "win":
   import msvcrt
elif sys_platform[:5] == "linux":
    import atexit
    atexit.register(Util.set_normal_term)
    Util.set_curses_term()

#The PSO Core
class PSO(object):
    
    #The Singleton instance
    _iInstance = None
    
    class Singleton:        
        ##Constructor of PSO
        #@param seed
        #@param interactiveMode  
        def __init__(self,seed=None,interactiveMode=True):
            #Random seed
            random.seed(seed)
            #Pso type used by particle.
            self.psoType = Consts.CDefPsoType 
            #Topology used (Must be created by using Topology base class)
            self.topology = None
            #Cognitive and Social Coefficients
            self.C1,self.C2 = Consts.CDefCoefficients
            #Time steps
            self.timeSteps = Consts.CDefSteps
            #Interactive Mode (True or False)
            self.interactiveMode = interactiveMode
            #Current step
            self.currentStep = 0
            #Fitness Evaluator
            self.function = None
            #Inertia Factor Minus
            self.inertiaFactorMinus = None
            #Inertia coefficient
            self.inertiaFactor = None
            #Time initial
            self.time_init = None
            #List of position boundary
            self.positionBounds = []
            #List of initial position boundary arrays
            self.initialPositionBounds = []
            #List of absolute velocity bounds 
            self.velocityBounds = []
            #Optimization type
            self.minimax = Consts.minimaxType["minimize"]
            #Report file adapter 
            self.reportAdapter = None
            #print "A PSO Engine was created, timeSteps=% d" % ( self.timeSteps, )
        
        #Set the function fitness
        def setFunction(self,function):
            self.function = function
        
        #@return the function
        def getFunction(self):
            return self.function
        
        #@return the function name
        def getFunctionName(self):
            return self.function.__name__
        
        #Sets the optimization type (Minimize or Maximize)
        #@param minima: The optimization type
        def setMinimax(self,minimax):
            if minimax not in Consts.minimaxType.values():
                Util.raiseException("Optimization type must be Maximize or Minimize !",TypeError)
            self.minimax = minimax
        
        #@return the minimax type
        def getMinimaxType(self):
            for key,value in Consts.minimaxType.items():
                if value == self.minimax:
                    return key
            return ""
          
        #Sets the psoType, use Consts.psoType (Basic, Constricted , Inertia)
        #@param psoType: The PSO type, from Consts.psoType
        def setPsoType(self,psoType):
            if psoType not in Consts.psoType.values():
                Util.raiseException("PsoType must be implemented !",TypeError)
            self.psoType = psoType
        
        #@return  the PsoType
        def getPsoType(self):
            for key,value in Consts.psoType.items():
                if value == self.psoType:
                    return key
            return ""
        
        #Sets the Topology and its parameters
        #@param topology: The current topology
        def setTopology(self,topology):
            self.topology = topology
            
        #@return the topology
        def getTopology(self):
            return self.topology
        #@return the name of the topology
        def getTopologyType(self):
            return self.topology.__class__.__name__ 
        
        #Initialize position and velocity bounds
        #@param dimensions the number of dimensions used
        def initializeBounds(self,dimensions):
            for i in xrange(dimensions):
                self.initialPositionBounds.append((0.0,0.0))
                self.positionBounds.append((0.0,0.0))
                self.velocityBounds.append(0.0)
        
        #Defines the entire search space
        #@param firstDimension firts dimension to set bound
        #@param lastDimension last dimension to set bound
        #@param minValue minimum/maximum bound value
        def definePositionBounds(self,firstDimension,lastDimension,minMaxValue):
            if type(minMaxValue) is not tuple:
                Util.raiseException("minMaxValue type must be a tuple (a,b).", TypeError)
            for i in range(firstDimension,lastDimension):
                self.positionBounds[i] = minMaxValue
        
        #Defines the search space region of the initial particles
        #@param firstDimension firts dimension to set bound
        #@param lastDimension last dimension to set bound
        #@param minValue minimum/maximum bound value
        def defineInitialPositionBounds(self,firstDimension,lastDimension,minMaxValue):
            if type(minMaxValue) is not tuple:
                Util.raiseException("minMaxValue type must be a tuple (a,b).", TypeError)
            for i in range(firstDimension,lastDimension):
                self.initialPositionBounds[i] = minMaxValue
        
        #@return the Time steps
        def getTimeSteps(self):
            return self.timeSteps
        
        #Sets the number of steps to converge
        #@param num_steps: the number of steps
        def setTimeSteps(self,num_steps):
            if num_steps < 1:
                Util.raiseException("Number of steps must be >=1",ValueError)
            self.timeSteps = num_steps
        
        #Defines the velocity bounds
        #@param firstDimension first dimension to be set
        #@param lastDimension last dimension to be set
        #@param value bound value
        def defineVelocityBounds(self,firstDimensiom,lastDimensiom,value):
            for i in range(firstDimensiom,lastDimensiom):
                self.velocityBounds[i] = value
        
        #Define the  inertiaFactorStart/End to set
        #@param inertiaFactorStart: The initial inertia factor coefficient
        #@param  inertiaFactorEnd: The  inertia factor coefficient at the end
        def setInitialInertiaFactor(self,inertiaFactorStart = Consts.CDefInertiaFactorStart, inertiaFactorEnd = Consts.CDefInertiaFactorEnd):
            if self.psoType == Consts.psoType["INERTIA"]:
                self.inertiaFactorMinus = abs((inertiaFactorStart - inertiaFactorEnd)) / self.timeSteps
                self.inertiaFactor = inertiaFactorStart
        
        #Updates the inertia factor (Only used by INERTIA Pso Type)
        def updateInertiaFactor(self):
            self.inertiaFactor = self.inertiaFactor - self.inertiaFactorMinus
        
        #Get the inertia factor(Only used by INERTIA Pso Type)    
        def getInertiaFactor(self):
            return self.inertiaFactor
        
        #Sets the Report Adapater of the PSO Engine (Warning: The use of the Report Adapter can redue the speed performance of the PSO.)
        #@param repadapter : one of the ReportAdapters classes instance
        def setReportAdapter(self,repadapter):
            self.reportAdapter = repadapter
        
        #Gets the Report Adapter of the PSO Engine
        #@return  a instance from one of the ReportAdapters classes
        def getReportAdapter(self):
            return self.reportAdapter
        
        #Gets the Topology/Swarm statistics class instance of the current iteration
        #@return tuple (topology,swarm) statitics class instances.
        def getStatistics(self):
            return self.topology.getStatistics()
        
        #Dumps the current statistics to the report adapter
        def dumpStatsReport(self):
            self.topology.statistics()
            self.reportAdapter.insert(self.getStatistics(), self.topology, self.currentStep)
           
        #The string representation of the PSO Engine"
        def __repr__(self):
            ret =   "- PSO-%s-%s Execution\n" % (self.getTopologyType(),self.getPsoType())
            ret +=  "\tSwarm Size:\t %d\n" % (self.topology.swarmSize,)
            ret +=  "\tDimensions:\t %d\n" % (self.topology.dimensions,)
            ret +=  "\tTime Steps:\t %d\n" % (self.timeSteps,)      
            ret +=  "\tCurrent Step:\t %d\n" % (self.currentStep,)
            ret +=  "\tMinimax Type:\t %s\n" % (self.getMinimaxType(),)
            ret +=  "\tFunction:\t %s\n" % (self.getFunctionName(),)
            ret +=  "\tReport Adapter:\t %s\n" % (self.reportAdapter,)
            ret +="\n"
            return ret
        
        #Do all the PSO execution until the termination criteria, accepts
        #the freq_stats (default is 0 to dump statistics at n-timeStep
        #@param freq_stats: If greater than 0, the statistics will be printed every freq_stats time Step.
        def execute(self,freq_stats=0):
            #Check the parameters set
            self.checkParametersSet()
            #Start time
            self.time_init = time()
            #Creates a new report if reportAdapter is not None.
            if self.reportAdapter: self.reportAdapter.open()
            #Initialize the PSO Engine
            self.initialize()
            
            print "Starting loop over evolutionary algorithm."
            
            try:
                while not self.constructSolution():
                    if freq_stats != 0:
                        if (self.currentStep % freq_stats == 0) or (self.currentStep == 1):
                            self.printStats()
                        
                        if self.reportAdapter:
                            if self.currentStep % self.reportAdapter.statsGenFreq == 0:
                                self.dumpStatsReport()
                        
                        if self.interactiveMode:
                            if sys_platform[:3] == "win":
                                if msvcrt.kbhit():
                                    if ord(msvcrt.getch()) == Consts.CDefESCKey:
                                        print "Loading modules for Interactive mode...",
                                        import pypso.Interaction
                                        print "done!\n"
                                        interact_banner = "## PyPSO v.%s - Interactive Mode ##\nPress CTRL-Z to quit interactive mode." % (pypso.__version__,)
                                        session_locals = {  "pso_engine"  : self,
                                                            "topology" : self.getTopology(),
                                                            "swarm_statistics": self.getTopology().swarmStats,
                                                            "topology_statistics": self.getTopology().topologyStats,
                                                            "pypso"   : pypso ,
                                                            "it"         : pypso.Interaction}
                                        print
                                        code.interact(interact_banner, local=session_locals)
                            elif sys_platform[:5] == "linux":
                                if Util.kbhit():
                                    if ord(Util.getch()) == Consts.CDefESCKey:
                                        print "Loading modules for Interactive mode...",
                                        import pypso.Interaction
                                        print "done!\n"
                                        interact_banner = "## PyPSO v.%s - Interactive Mode ##\nPress CTRL-D to quit interactive mode." % (pypso.__version__,)
                                        session_locals = {  "pso_engine"  : self,
                                                            "topology" : self.getTopology(),
                                                            "swarm_statistics": self.getTopology().swarmStats,
                                                            "topology_statistics": self.getTopology().topologyStats,
                                                            "pypso"   : pypso ,
                                                            "it"         : pypso.Interaction}
                                        print
                                        code.interact(interact_banner, local=session_locals)
                                            
            except KeyboardInterrupt:
                print "\n\tA break was detected, you have interrupted the evolution !\n"
     
            if freq_stats != 0:
                self.printStats()
                self.printTimeElapsed()
            
            if self.reportAdapter:
                if (self.currentStep % self.reportAdapter.statsGenFreq == 0):
                    self.dumpStatsReport()
                    self.reportAdapter.saveAndClose()
                                    
        #Constructs a solution (one step of the proccess).
        def constructSolution(self):
            self.topology.updateParticlesPosition()
            self.topology.updateParticlesInformation()

            if type(self.topology) is pypso.LocalTopology.LocalTopology:
                self.topology.storeBestParticle()
            #print 'Updating topology position and information.'
            
            if self.psoType == Consts.psoType["INERTIA"]:
                self.updateInertiaFactor()
                #print "Updated the inertia factor"
            
            self.currentStep += 1
        
            #print "The swarm update %d was finished."  % (self.currentStep,)
            return (self.currentStep == self.timeSteps)        
              
        #Initializes the PSO Engine. Create and initialize the swarm   
        def initialize(self):
            self.topology.initialize()
            print "The PSO Engine was initialized !"
        
        #Check all the parameters set before running the engine.    
        def checkParametersSet(self):
            if not self.topology or not self.function:
                Util.raiseException("Topology/Evaluation fuction not yet defined.", TypeError)
            if self.psoType == Consts.psoType["INERTIA"]:
                if not self.inertiaFactorMinus or not self.inertiaFactor:
                    Util.raiseException("Set the setInitialInertiaFactor() for the Inertia weight.", TypeError)
            if not self.initialPositionBounds or not self.velocityBounds or not self.positionBounds:
                 Util.raiseException("The Position/Velocity/InitialPos Bounds not yet defined.", TypeError)
        
        #Print the swarm statistics
        def printStats(self):
            percent = self.currentStep * 100 / float(self.timeSteps)
            message = "Step: %d (%.2f%%):" % (self.currentStep, percent)
            print message,
            self.topology.statistics()
            self.topology.printStats()
        
        #Shows the time elapsed since the beginning of the solution construction
        def printTimeElapsed(self):
            print "Total time elapsed: %.3f seconds." % (time()-self.time_init)



    def __init__(self):
        #Check whether we already have an instance
        if PSO._iInstance is None:
            #Create and remember the instance
            PSO._iInstance = PSO.Singleton()
        #Store instane reference as the only member  in the handle
        self.__dict__['EventHandler_instance'] = PSO._iInstance
    
    ##Delegate access to implementation
    #@param attr Attribute wanted.
    #@return Attribute
    def __getattr__(self,aAttr):
        return getattr(self._iInstance,aAttr)
    
    ##Delegate access to implementation
    def __setattr__(self,aAttr,aValue):
        return setattr(self._iInstance,aAttr,aValue)
    
    def __repr__(self):
        return self._iInstance.__repr__()
                
