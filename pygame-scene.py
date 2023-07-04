import Sofa
import Sofa.SofaGL as SG
import Sofa.Core as SC
import Sofa.Simulation as SS
import SofaRuntime
import os
import time
sofa_directory = os.environ["SOFA_ROOT"]
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Directory to the different logos
logo_dir = "logos/kings-logo.png"

# Create the pygame widnow size and flags for debugging and final demo
display_size = (1920, 1080)
deb_flags = pygame.DOUBLEBUF | pygame.OPENGL
flags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN

class ImageLoader:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.img_data = 0
    
    def load(self, im_dir):
        image = pygame.image.load(im_dir).convert_alpha()
        img_data = pygame.image.tostring(image, 'RGBA')
        self.width = image.get_width()
        self.height = image.get_height()

        self.texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)     

    def draw(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(self.x, self.y, 0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)
        glTexCoord2f(0, 1)
        glVertex2f(0, self.height)
        glEnd()
        glDisable(GL_TEXTURE_2D)


def init_display(node: SC.Node, im_loader: ImageLoader):
    """
    Define the initial window for the pygame rendering

    Args:
        node (SC.Node): Root node for a Sofa simulation scene
    """
    pygame.display.init()
    pygame.display.set_mode(display_size, deb_flags)
    pygame.display.set_caption("Pygame logo")
    # pygame.mouse.set_visible(False)
    glClearColor(1, 1, 1, 1)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, display_size[0], display_size[1], 1)
    glMatrixMode(GL_MODELVIEW)

    # Draw the logo
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    im_loader.load(logo_dir)
    im_loader.draw()

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    SG.glewInit()
    SS.initVisual(node)
    SS.initTextures(node)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display_size[0] / display_size[1]), 0.1, 50.0)
    
    # Set the background to white
    # glClearColor(1, 1, 1, 1)
    # glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    pygame.display.flip()

def simple_render(rootNode: SC.Node, im_loader: ImageLoader):
    """
    Get the OpenGL context to render an image of the simulation state

    Args:
        rootNode (SC.Node): Sofa root node 
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, display_size[0], display_size[1], 1)
    glMatrixMode(GL_MODELVIEW)

    # Draw the logo
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    im_loader.draw()

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display_size[0] / display_size[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    cameraMVM = rootNode.camera.getOpenGLModelViewMatrix()
    glMultMatrixd(cameraMVM)
    SG.draw(rootNode)

    pygame.display.flip()



def createScene(root: SC.Node):
    """
    This function is necessary to run Sofa from both the runSofa executable and the python interpreter (IDE)

    Args:
        root (SC.Node): Root node for a Sofa simulation scene
    """
    # Register all the common component in the factory.
    SofaRuntime.PluginRepository.addFirstPath(os.path.join(sofa_directory, 'bin'))
    root.addObject("RequiredPlugin", name="Sofa.Component.IO.Mesh")
    root.addObject("RequiredPlugin", name="Sofa.Component.Engine.Transform")
    root.addObject("RequiredPlugin", name="Sofa.Component.LinearSolver.Direct")
    root.addObject("RequiredPlugin", name="Sofa.Component.Mass")
    root.addObject("RequiredPlugin", name="Sofa.Component.ODESolver.Backward")
    root.addObject("RequiredPlugin", name="Sofa.Component.SolidMechanics.Spring")
    root.addObject("RequiredPlugin", name="Sofa.Component.StateContainer")
    root.addObject("RequiredPlugin", name="Sofa.Component.Topology.Container.Constant")
    root.addObject("RequiredPlugin", name="Sofa.Component.Visual")
    root.addObject("RequiredPlugin", name="Sofa.GL.Component.Rendering3D")
    root.addObject("RequiredPlugin", name="SofaConstraint")
    root.addObject("RequiredPlugin", name="SofaHaptics")
    root.addObject("RequiredPlugin", name="SofaMeshCollision")
    root.addObject("RequiredPlugin", name="SofaUserInteraction")
    root.addObject("RequiredPlugin", name="Sofa.Component.SceneUtility")
    root.addObject("RequiredPlugin", name="SofaPython3")

    # place light and a camera
    root.addObject("LightManager")
    root.addObject("DirectionalLight", direction=[0,1,0])
    root.addObject("InteractiveCamera", name="camera", position=[0,17.5,0],
                            lookAt=[0,0,0], distance=30,
                            fieldOfView=45, zNear=0.63, zFar=55.69)
    
    sphere = root.addChild("Sphere")
    sphere.addObject("MeshObjLoader", name="loader", filename="mesh/sphere.obj")
    sphere.addObject("OglModel", src="@loader", color="white")

def main():
    SofaRuntime.importPlugin("SofaComponentAll")
    im_loader=ImageLoader(640, 400)
    root = SC.Node("root")
    createScene(root)
    SS.init(root)
    init_display(root, im_loader)
    done = False

    while not done:
        SS.animate(root, root.getDt())
        SS.updateVisual(root)
        simple_render(root, im_loader)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break
        time.sleep(root.getDt())

    pygame.quit()
if __name__ == "__main__":
    main()