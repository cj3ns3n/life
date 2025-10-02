class Move:
  def __init__(self, dir):
    self.dir = dir

class Talk:
  def __init__(self, dir, message):
    self.dir = dir
    self.message = message

class EndConversation:
  pass

class GiveFood:
  def __init__(self, dir, amount):
    self.dir = dir
    self.amount = amount

class Attack:
  def __init__(self, dir):
    self.dir = dir
    