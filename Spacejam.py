from direct.showbase.ShowBase import ShowBase
import math, sys, random
import DefensePaths as defensePaths
import SpaceJamClasses as SpaceJamClasses
from panda3d.core import Vec3


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.SetupScene()
        self.SetKeyBindings()
        self.taskMgr.add(self.SpawnDronesTask, "SpawnDronesTask")
        self.taskMgr.add(self.UpdateCamera, "UpdateCamera")

        #test code for freecam
        self.freeCamera = False
    def SetupScene(self):
    
        self.Universe = SpaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.obj", self.render, 'Universe', "Assets/Universe/Universe2.jpg", (0, 0, 0), 18008)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/WaterPlanet2.png", (-6000, -3000, -800), 250)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2', "./Assets/Planets/1.png", (0, 6000, 0), 300)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3', "./Assets/Planets/cheeseplanet.png", (500, -5000, 200), 500) 
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4', "./Assets/Planets/grplanet.png", (300, 6000, 500), 150) 
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5', "./Assets/Planets/redmoon.png", (700, -2000, 100), 500)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6', "./Assets/Planets/planet3.jpg", (0, -980, -1480), 780)
        self.SpaceStation1 = SpaceJamClasses.SpaceStation(self.loader, "./Assets/SpaceStation/spaceStation.x", self.render, 'SpaceStation1', "./Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1800, -100), 40)

        # Pass taskMgr to Spaceship so it can move!
        self.Hero = SpaceJamClasses.Spaceship(self.loader, "Assets/Spaceships/spacejet.3ds", self.render, 'Hero', 
                                             "Assets/Spaceships/spacejet_C.png", Vec3(1000, 1200, -58), 58, self.taskMgr, self.camera)

    def SetKeyBindings(self):
        
        self.accept('w', self.Hero.move_forward, [1])    
        self.accept('w-up', self.Hero.move_forward, [0])  
        self.accept('a', self.Hero.turn_left, [1])       
        self.accept('a-up', self.Hero.turn_left, [0])     
        self.accept('d', self.Hero.turn_right, [1])      
        self.accept('d-up', self.Hero.turn_right, [0])    
        self.accept('s', self.Hero.turn_down, [1])       
        self.accept('s-up', self.Hero.turn_down, [0])     
        self.accept('q', self.Hero.roll_left, [1])       
        self.accept('q-up', self.Hero.roll_left, [0])     
        self.accept('e', self.Hero.roll_right, [1])      
        self.accept('e-up', self.Hero.roll_right, [0])    

        self.accept('z', self.Hero.zoom_out, [1])  # Hold 'z' to zoom out
        self.accept('z-up', self.Hero.zoom_out, [0])
        self.accept('x', self.Hero.zoom_in, [1])  # Hold 'x' to zoom in
        self.accept('x-up', self.Hero.zoom_in, [0])
        #freecam
        self.accept('f', self.ToggleFreeCamera)

    def UpdateCamera(self, task):
    # Get the spaceship's current position and rotation
        if not self.freeCamera:
        # Follow the spaceship
            ship_pos = self.Hero.modelNode.getPos()
            ship_quat = self.Hero.modelNode.getQuat()

            offset = Vec3(0, 30, 10)  # Adjust values as needed
            offset = ship_quat.xform(offset)  

            self.camera.setFluidPos(ship_pos + offset)
            self.camera.setQuat(ship_quat)

        return task.cont

    def ToggleFreeCamera(self):
        self.freeCamera = not self.freeCamera
        if self.freeCamera:
            print("Free camera mode enabled.")
        else:
            print("Free camera mode disabled, camera following ship.")

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius=1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B=0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
    
        drone = SpaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, 
                                  "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
        drone.modelNode.reparentTo(self.render)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
    
        drone = SpaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, 
                                  "./Assets/DroneDefender/octotoad1_auv.png", position, 10)
        drone.modelNode.reparentTo(self.render)
        
    def SpawnDronesTask(self, task):
        
        if SpaceJamClasses.Drone.droneCount >= 60:
            return task.done
        
        SpaceJamClasses.Drone.droneCount += 1
        nickName = f"Drone{SpaceJamClasses.Drone.droneCount}"
        
        # Alternating drone spawns
        if SpaceJamClasses.Drone.droneCount % 2 == 0:
            self.DrawCloudDefense(self.Planet1, nickName)
        else:
            self.DrawBaseballSeams(self.SpaceStation1, nickName, SpaceJamClasses.Drone.droneCount, 60, 2)

        return task.cont


app = MyApp()
app.run()
