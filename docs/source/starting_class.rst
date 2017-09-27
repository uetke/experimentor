Starting a new Experiment
=========================
When starting a new experiment, after defining the YAML files with the information needed, we need to feed them to Python
in order to interpret them and communicate with the devices accordingly. Some common tasks will always be present when
starting a new experiment, for example transforming a :code:`yml` file to a dictionary, or storing the different steps
specified in a class. These basic steps are already defined in the :code:`base_experiment` module, and therefore any
new experiments need to be subclasses of it. For a snapshot, you can check the examples folder.

Subclassing the Experiment
**************************
Subclassing is a very important topic that every person programming with Python should at least be familiar with. If we
are starting a new experiment called for example :code:`laser_scan`, we should start our own class like this::

   from experimentor.experiment.base_experiment import Experiment
   class LaserScan(Experiment):
      def __init__(self, measure):
         super().__init__(measure)

These four lines of code will make all the methods and properties of the base class experiment readily available in our own class. These methods include :code:`load_devices`, :code:`initialize_devices` and many others that you can check by reading the documentation of the class.

If we also import the :code:`from_yaml_to_dict`, we can already import the devices, actuators and sensors into the class
with the following few lines::

   devices = from_yaml_to_dict(self.init['devices'])
   actuators = from_yaml_to_dict(self.init['actuators'])
   sensors = from_yaml_to_dict(self.init['sensors'])
   self.load_devices(devices)
   self.load_sensors(sensors)
   self.load_actuators(actuators)
   self.initialize_devices()

It is important to note here that we are already acessing a property of the class, called :code:`self.init`. This property is generated automatically when loading the dictionary :code:`measure` through the base class. Remember from the previous chapter that the YML of our experiment had a section called init and was holding the location of the yml files with the devices, actuators and sensors.

The last line of the previous block of code initializes the devices. By looking at the :code:`Device` class, one can see that the initialization is done based on the connection type, and assuming that the device is a *Lantz* driver. If one wishes to add devices that need different parameters to be passed as arguments, or that are based in different technologies (for example at the time of writing TCP/IP devices were not yet implemented), those lines of code are the place to modify.

Now we have our class with devices, sensors and actuators. It is time to start adding different features to it in order to make a measurement.

.. automodule:: experimentor.lib.general_functions
   :members:
