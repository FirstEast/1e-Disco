# ctypes for derpbit protocol.

import ctypes
from ctypes import c_uint8, c_uint16, c_uint32

BROADCAST_PORT = 7331
PIXEL_PORT = 9897

class DeviceType():
  ETHERDREAM = 0
  LUMIABRIDGE = 1
  PIXELPUSHER = 2

class DiscoveryPacketHeader(ctypes.Structure):
  _fields_ = [
    (u"mac_address", c_uint8 * 6),
    (u"ip_address", c_uint8 * 4),
    (u"device_type", c_uint8),
    (u"protocol_version", c_uint8),
    (u"vendor_id", c_uint8),
    (u"product_id", c_uint16),
    (u"hw_revision", c_uint16),
    (u"sw_revision", c_uint16),
    (u"link_speed", c_uint32)
  ]

  def mac_str(self):
    return u"%x%x%x%x%x%x" % tuple(self.mac_address)

  def ip_str(self):
    return u"%d.%d.%d.%d" % tuple(self.ip_address)

class PixelPusher(ctypes.Structure):
  _fields_ = [
    (u'strips_attached', c_uint8),
    (u'max_strips_per_packet', c_uint8),
    (u'pixels_per_strip', c_uint16),
    (u'update_period', c_uint32),   # microseconds
    (u'power_total', c_uint32),     # pwm units
    (u'delta_sequence', c_uint32),  # difference between received and expected sequence numbers
    (u'controller_ordinal', c_uint32), # ordering number for this controller.
    (u'group_ordinal', c_uint32),
    (u'artnet_uinverse', c_uint16), # configured artnet starting point for this controller
    (u'artnet_channel', c_uint16),
    (u'my_port', c_uint16),
    (u'strip_flags', c_uint8 * 8), # flags for each strip, for up to eight strips
    (u'pusher_flags', c_uint32),
    (u'segments', c_uint32),
  ]

class LumiaBridge(ctypes.Structure):
  _fields_ = []

class EtherDream(ctypes.Structure):
  _fields_ = [
    (u"buffer_capacity", c_uint16),
    (u"max_point_rate", c_uint32),
    (u"light_engine_state", c_uint8),
    (u"playback_state", c_uint8),
    (u"source", c_uint8),
    (u"light_engine_flags", c_uint16),
    (u"buffer_fullness", c_uint16),
    (u"point_rate", c_uint32),
    (u"point_count", c_uint32)
  ]

class Particulars(ctypes.Union):
  _fields_ = [
    (u"pixelpusher", PixelPusher),
    (u"lumiabridge", LumiaBridge),
    (u"etherdream", EtherDream)
  ]

class DiscoveryPacket(ctypes.Structure):
  _fields_ = [(u"header", DiscoveryPacketHeader),
              (u"p", Particulars)]
  @classmethod
  def size(cls):
    return ctypes.sizeof(cls)
