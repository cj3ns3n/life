import argparse
from world import World
from engine import Engine

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='chatGPT inspired life simulation')

  world = World()
  engine = Engine(world)

  engine.run()
# end if

  
