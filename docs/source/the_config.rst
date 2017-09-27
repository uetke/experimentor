Config Parameters
=================
Some configuration parameters are handier to define in a broad way than individually each time an experiment is
developed. These configuration parameters normally are details that shouldn't matter to a casual user, but that may have
un intended consequences for people dealing with very specific setups and trying to push the limits of their devices.

The Experimentor possesses a module called Config, that is actually just a class with some parameters defined outside
the :code:`__init__` method. This is particularly handy because the parameters can be altered at runtime, before the
module if imported by other objects. For example, if one defines this in config.py::

   class Config:
      param_a = 1

And we write a module that uses that config, module.py::

   from config import Config
   def use_config():
      print(Config.param_a)

And later on, from a different file, lets say start.py::

   from config import Config
   from module import use_config
   Config.param_a = 2
   use_config()

.. automodule:: experimentor.config.config

.. autoclass:: experimentor.config.config.Config
    :members: