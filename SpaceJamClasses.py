from panda3d.core import NodePath, Vec3, CollisionNode, CollisionSphere, CollisionHandlerQueue, CollisionRay
import random, math
from direct.task import Task

class Universe:
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        
        

class Planet:
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone:
    droneCount = 0
    dronePool = []  # Pool of recycled drones

    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        if Drone.dronePool:
            # Recycle a drone from the pool
            self.modelNode = Drone.dronePool.pop()
            self.modelNode.reparentTo(parentNode)
        else:
            # Create a new drone
            self.modelNode = loader.loadModel(modelPath)
            self.modelNode.setName(nodeName)

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        Drone.droneCount += 1
        self.collisionNode = self.create_collision_node()

    def create_collision_node(self):
        """Adds a collision sphere to the drone."""
        collision_node = CollisionNode(f"drone-collision-{Drone.droneCount}")
        collision_node.addSolid(CollisionSphere(0, 0, 0, 5))  # Adjust the radius as needed
        collision_node.setFromCollideMask(1)  # Can be customized to only collide with specific objects
        return self.modelNode.attachNewNode(collision_node)

    @staticmethod
    def return_to_pool(drone):
        """Returns the drone to the pool when it is destroyed."""
        Drone.dronePool.append(drone.modelNode)
        drone.modelNode.removeNode()


class SpaceStation:
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

    

class Spaceship:
    def __init__(self, loader, modelPath, parentNode, nodeName, texPath, posVec, scaleVec, taskMgr, camera):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        
        self.taskMgr = taskMgr  # For managing tasks
        self.camera = camera    # Pass the camera reference from MyApp to Spaceship
        self.zoom_factor = 5    # Control how much the camera zooms in and out
        self.cameraZoomSpeed = 10
        
    def move_forward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyMoveForward, 'move-forward')
        else:
            self.taskMgr.remove('move-forward')

    def ApplyMoveForward(self, task):
        rate = 5
        direction = self.modelNode.getQuat().getForward()
        self.modelNode.setPos(self.modelNode.getPos() + direction * rate)
        return Task.cont

    def turn_left(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyTurnLeft, 'turn-left')
        else:
            self.taskMgr.remove('turn-left')

    def ApplyTurnLeft(self, task):
        self.modelNode.setH(self.modelNode.getH() + 1.5)
        return Task.cont

    def turn_right(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyTurnRight, 'turn-right')
        else:
            self.taskMgr.remove('turn-right')

    def ApplyTurnRight(self, task):
        self.modelNode.setH(self.modelNode.getH() - 1.5)
        return Task.cont

    def turn_up(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyTurnUp, 'turn-up')
        else:
            self.taskMgr.remove('turn-up')

    def ApplyTurnUp(self, task):
        self.modelNode.setP(self.modelNode.getP() - 1.5)  # Upward tilt (pitch)
        return Task.cont

    def turn_down(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyTurnDown, 'turn-down')
        else:
            self.taskMgr.remove('turn-down')

    def ApplyTurnDown(self, task):
        self.modelNode.setP(self.modelNode.getP() + 1.5)  # Downward tilt (pitch)
        return Task.cont

    def roll_left(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollLeft, 'roll-left')
        else:
            self.taskMgr.remove('roll-left')

    def ApplyRollLeft(self, task):
        self.modelNode.setR(self.modelNode.getR() + 2.0)  # Roll left
        return Task.cont

    def roll_right(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollRight, 'roll-right')
        else:
            self.taskMgr.remove('roll-right')

    def ApplyRollRight(self, task):
        self.modelNode.setR(self.modelNode.getR() - 2.0)  # Roll right
        return Task.cont

    def UpdateCamera(self, task):
        """Keeps the camera following the spaceship with smooth transition."""
        target_pos = self.modelNode.getPos() + Vec3(0, -30, 10)
        current_pos = self.camera.getPos()
        new_pos = current_pos + (target_pos - current_pos) * 0.1  # Smooth transition
        self.camera.setPos(new_pos)
        self.camera.lookAt(self.modelNode)
        return task.cont

    def set_camera(self):
        """Directly sets the camera's position."""
        self.UpdateCamera(None)

    def zoom_in(self, keyDown):
        """Zoom the camera in (closer to the spaceship)."""
        if keyDown:
            self.taskMgr.add(self.ApplyZoomIn, 'zoom-in')
        else:
            self.taskMgr.remove('zoom-in')

    def ApplyZoomIn(self, task):
        # Move camera 1 unit closer along the z-axis (camera's forward direction)
        current_pos = self.camera.getPos()
        self.camera.setPos(self.camera.getPos() + Vec3(0, self.cameraZoomSpeed, 0))  # Adjust for zoom in
        return Task.cont

    def zoom_out(self, keyDown):
        """Zoom the camera out (further away from the spaceship)."""
        if keyDown:
            self.taskMgr.add(self.ApplyZoomOut, 'zoom-out')
        else:
            self.taskMgr.remove('zoom-out')

    def ApplyZoomOut(self, task):
        # Move camera 1 unit further along the z-axis (camera's backward direction)
        current_pos = self.camera.getPos()
        self.camera.setPos(self.camera.getPos() + Vec3(0, -self.cameraZoomSpeed, 0))  # Adjust for zoom out
        return Task.cont

def create_drone_circle(centralObject, numDrones, axis='x', radius=1):
    """Creates a formation of drones in a circle around an object."""
    angleStep = 2 * math.pi / numDrones
    
    for i in range(numDrones):
        angle = i * angleStep
        position = Vec3()

        if axis == 'x':
            position.setX(math.cos(angle) * radius)
            position.setY(random.uniform(-0.5, 0.5))
            position.setZ(random.uniform(-0.5, 0.5))
        elif axis == 'y':
            position.setX(random.uniform(-0.5, 0.5))
            position.setY(math.cos(angle) * radius)
            position.setZ(random.uniform(-0.5, 0.5))
        else:  # axis == 'z'
            position.setX(random.uniform(-0.5, 0.5))
            position.setY(random.uniform(-0.5, 0.5))
            position.setZ(math.cos(angle) * radius)
        
        position += centralObject.modelNode.getPos()

        Drone(
            centralObject.loader,
            "./Assets/DroneDefender/DroneDefender.obj",
            centralObject.render,
            f"Drone-{i}",
            "./Assets/DroneDefender/octotoad1_auv.png",
            position,
            5
        )

