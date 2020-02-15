import os, sys, inspect
srcDir = os.path.dirname(inspect.getfile(inspect.currentframe()))
libDir = os.path.abspath(os.path.join(srcDir, '../lib/x86'))
sys.path.insert(0, libDir)
import Leap



class SampleListener(Leap.Listener):
  def on_connect(self, controller):
    print('lsdjfdsklfj')

  def on_frame(self, controller):
    frame = controller.frame()
    hands = frame.hands
    fingers = frame.fingers
    print('# of hands:', len(hands),
    '# of fingers:', len(fingers))
    
    for hand in hands:
      print('x', hand.basis.x_basis.x,
            'y', hand.basis.y_basis,
            'x', hand.basis.z_basis)

def main():

  controller = Leap.Controller()
  listener = SampleListener()
  controller.add_listener(listener)

  print('Press enter to quit: ')
  sys.stdin.readline()

if __name__ == '__main__':
  main()