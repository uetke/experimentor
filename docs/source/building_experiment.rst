Building your first experiment
==============================

In the previous chapter we have dealt on how to start writing the YML files that are needed for the overal layout of the experiment. In this chapter we are going to focus on how to load them into different Python classes. The examples that we are going to develop in this section are based on the example `laser_scan`. The differences with the working example (for instance the lack of docstrings and of logging), shouldn't be crucial and are only meant to make the code slightly more compact.

The Experiment class
~~~~~~~~~~~~~~~~~~~~
To start, we need to create a subclass of the base experiment class. This will bring along some useful methods and properties. To do so, we create a new file and add the following::

   from experimentor.experiment.base_experiment import Experiment


   class LaserScan(Experiment):
    def __init__(self, measure):
        super().__init__(measure)

.. note:: At this point is clear that you should have already some experience with Python classes and inheritance. I suggest you to read about those two concepts if you have never heard of them before.

These few lines are enough to start working forward. The way the base experiment works is by reading the dictionary passed (measure) and storing each main key as a property of the class itself. It is therefore possible to access, for example, the `scan` block by just typing::

   self.scan

In turn this will be a dictionary with all the parameters set in the config YML file. At this point we need to load the devices into the experiment. The next few lines show how to do it::

   from experimentor.lib.general_functions import from_yaml_to_dict
   [...]
         devices = from_yaml_to_dict(self.init['devices'])
         actuators = from_yaml_to_dict(self.init['actuators'])
         sensors = from_yaml_to_dict(self.init['sensors'])

.. note:: To focus slowly in the code, it is important that you interpret correctly whay is going on. In this case, the `[...]` denotes a piece of missing code because it was stated right before; the definition of the class and the __init__ are missing. If it is not clear how it should look like, it is better that you check the example once in a while. Whenever possible, I keep the indentation as it should be.

The function `from_yaml_to_dict` only translates a yaml file to a dictionary, nothing fancy. Remember that in the previous chapter we defined the location of the files with the devices, actuators and sensors? Now we are putting them into practice! Now that we have the dictionaries of devices and sensors, we need to make something out of them. As you know, sensors and actuators are plugged to devices, and therefore it is handy to reproduce this hierarchical structure in the code. The base class `Experiment` has some methods to assist us. We should just type::

           self.load_devices(devices)
           self.load_sensors(sensors)
           self.load_actuators(actuators)

These three methods were inherited from the Experiment class. When the `load_devices` is called, the function will iterate over each key and will add the corresponding `Device` to a dictionary. So, if we defined a National Instruments device like specified in the previous chapter, you can access it like so::

   self.devices['NI-DAQ']

Now, the dictionary devices will store more information than just the device; it will also store all the sensors and actuators connected to the device. You can access them like this::

   dev = self.devices['NI-DAQ']['dev']
   sensors = self.devices['NI-DAQ']['sensors']
   actuators = self.devices['NI-DAQ']['actuators']

in this example, dev is a Device object (you can check its own documentation later), while sensors and actuators are dictionaries, holding a Sensor or Actuator object for each key.

The only missing thing is to initialize the driver of each device::

         self.initialize_devices()

Now the heavy part of initializing the class is done. We have our dictionary of devices, and each devices has sensors and actuators connected to it. What we have to do next is to prepare for a measurement.

Setting up a scan
~~~~~~~~~~~~~~~~~
Once we have the devices loaded, we want to prepare both the laser and the acquisition card to do a scan. Remember at this point that the laser drives the experiment; the acquisition card only digitizes a signal when the laser issues a trigger. In turn, the laser issues a trigger at specific intervals.

We start a new method and grabbed the properties of our scan::

    def setup_scan(self):
        # First setup the laser
        laser_params = self.scan['laser']['params']
        laser = self.devices[self.scan['laser']['name']]['dev']
        laser.apply_values(laser_params)

First, we are going to setup the laser. For it, we load the parameters stored in scan['laser']['params']. You can always refer to the yaml file to see what they are, add new ones if you realize something is missing, etc. Then we load the Device that corresponds to the laser, and hence why the last ['dev'] in the call. When we do `laser.apply_values`, we are actually using a method that belongs to the Device object. Bear in mind that `laser_params` is a dictionary, with 'property'=>'value' as a structure.

Bottom line is that you can pass a bunch of properties to a driver, provided that you do it through a dictionary. For example, you could have a dictionary like this::

   prop = {
      'wavelength': '1500nm',
      'power': '200mW',
   }

After setting the laser to what we need, we have to prepare our acquisition card. If we are dealing with National Instruments cards, a lot of different properties have to be set before reading from a channel. So, let's start step by step, specially because afterwards we will have to digg into the NI model class to understand what is happening. First, we need to define the number of points and the temporal accuracy of our measurement::

   num_points = 1+int(
        (laser.params['stop_wavelength'] - laser.params['start_wavelength']) / laser.params['interval_trigger'])

        # Estimated accuracy to set the DAQmx to.
        accuracy = laser.params['interval_trigger'] / laser.params['wavelength_speed']

        # Conditions to be passed to the DAQ.
        conditions = {
            'accuracy': accuracy,
            'points': num_points
        }

Remember that in this experiment, the ADQ is triggered by a signal coming from the laser. Therefore we can be sure of the number of points we are going to acquire per scan. The accuracy is just how much time there is between points. If the scan speed is constant, the time between acquisition points is given by distance/speed. In the case of triggering the digitalization from an external source, according to NI this parameter is not crucial but should be there anyhow.
