def enum(**enums):
    return type('Enum', (), enums)

ParameterTypes = enum(
  COLOR = 'color',
  STRING = 'string',
  NUMBER = 'number',
  BOOL = 'bool',
  IMAGE = 'image',
  GIF = 'gif',
  BEAT = 'beat'
)