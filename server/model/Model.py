class Model():
  def __init__(self, initial_data):
    self.attributes = initial_data
    self.listeners = {}

  def set(self, attr, value):
    if self.attributes[attr] != value:
      self.attributes[attr] = value

  def get(self, attr):
    return self.attributes[attr]

  def trigger(self, event, data):
    if event in self.listeners:
      for listener in self.listeners[event]:
        listener(self, data)

  def on(self, event, callback):
    if event in self.listeners:
      self.listeners[event].append(callback)
    else:
      self.listeners[event] = [callback]