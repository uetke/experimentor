Adding Methods to the Experiment
================================
Classes are useful when they have methods in them, and that is what we are going to do with our :code:`LaserScan` class
that we just wrote. Assuming we want to perform 1-D scan, i.e. to record a signal while we scan the wavelength of a
laser, we should start by setting up the laser and the DAQ card we are going to employ to record the data.

Set Up
******
Our first method is going to eloquently be called :code:`setup_scan`. We need first to grab the parameters of the scan
and pass them to the laser itself. We can do the following::

   laser_params = self.scan['laser']['params']
   laser = self.devices[self.scan['laser']['name']]['dev']
   laser.apply_values(laser_params)

Now, even if these are only three lines, what is exactly happening takes slightly longer. In the first line we are
calling the property scan, that was generated when loading the YML of the experiment itself. You can immediately see
that the structure of the yml comes in handy here, we are just reproducing it. Next, we need to fetch the laser from
the dictionary of devices that was generated in the previous chapter. Remember that devices are identified by their
names, while we are interested in the device itself, not the sensors or actuators associated with it. That is why we append the ['dev'] at the end.

The last step is just applying a dictionary of values to a device. In theory this is easy, but in practice a lot of
different things can happen. For instance, under the hood one needs to check what kind of device we are dealing with,
if it is a DAQ, most likely we are passing actuators as the key of the dictionary, while if it is a Lantz driver, we are
passing only the Features defined in the driver. Without entering into details here, it is worth noting that the method
:code:`apply_values` works in special conditions and needs to be further improved, specially when adding new devices.

Now we are halfway the setting up process; we need to set the daq to a state in which is ready to acquire. Setting up the daq is a delicate procedure, since differnt devices take different parameters. It is not the same setting up an oscilloscope, than an NI card or an Adwin box. I will focus on the NI card because they are widespread and it is what was developed together with the *PharosController* package.

For setting up the DAQs it is handy to employ a single dictionary in which all the different parameters are passed; I
normally called this dictionary :code:`conditions` and I use it both in the experiment class as in the DAQ model.
Amongst the things that need to be defined in order to make a timetrace of an analog signal, one has to define the
number of points and the accuracy, meaning the time between samples. Even if we are triggering the acquisition
externally, the NI cards need to know an estimate. We add the following to the code::

   num_points = 1+int(
      (laser.params['stop_wavelength'] - laser.params['start_wavelength']) / laser.params['interval_trigger'])

   accuracy = laser.params['interval_trigger'] / laser.params['wavelength_speed']

   conditions = {
      'accuracy': accuracy,
      'points': num_points
   }

I guess the above lines are self explanatory. The example file becomes a bit convoluted at this point, because it goes
through all devices to see which ones have sensors that need to be monitored. The example was developed keeping
generality in mind, but it is not needed when one already knows only one type of DAQ is going to be used. Assuming we
only have a NI card available and that we are going to use that one, we can do::

   device = 'NI-DAQ'
   dev = self.devices[device]['dev']
   sensors = []
   sens_to_monitor = self.scan['detectors'][device]

The first line is to explicitly select the DAQ we want; we get the Device from our own class, and the devices we need to
monitor from the YML file of the experiment. Skipping some verifications to see that the sensors was correctly declared,
etc. we can iterate through all the sensors and append them to the empty list just declared. This variable is going to
be added to the conditions dictionary and passed to the DAQ::

   for sensor in sens_to_monitor:
      s = self.devices[device]['sensors'][sensor]
      sensors.append(s)

   conditions.update({
      'sensors': sensors,
      'trigger': dev.properties['trigger'],
      'trigger_source': dev.properties['trigger_source'],
      'sampling': 'continuous',
   })

Here you see something very important happening. First, we use the method :code:`update` in order to update the
conditions without erasing what was previously set. Then, we are choosing the trigger and the trigger source from the
properties of the DAQ itself. This was a design choice that may or may not be the best for your experiment. If you have
an experiment that always uses the same trigger for the daq, then it is fine, but if you need to perform scans with
different triggers, you may better pass it as a parameter of your experiment rather than your device.

Finally, we need to pass the conditions collected to the DAQ, we need to do::

   daq_driver = dev.driver
   self.scan_task = daq_driver.analog_input_setup(conditions)

Since Devices can be of any kind, they only have the mosot basic methods defined. If one wants to access specific
methods or properties defined in the model, it has to be done via the :code:`driver` property directly. The
:code:`driver` is where the initialized class of the device is stored. Since we are using an external trigger, we can
also just trigger the DAQ, it will not do anything until the laser is also triggered::

   daq_driver.trigger_analog()

Triggering the laser
********************
The next method will just trigger the laser in order to do a wavelength scan while the DAQ is monitoring the specific signals. Small class, very important::

   laser = self.devices[monitor['laser']['name']]
   laser.driver.execute_sweep()


Reading the ADQ
***************
For reading the ADQ we need to follow steps similar than the ones for setting it up. We define the conditions for reading and get the data::

   conditions = {'points': -1}  # To read all the daq points available
   data = {}
   device = 'NI-DAQ'
   dev = self.devices[device]['dev']
   daq_driver = dev.driver
   num_sensors = len(self.scan['detectors'][device])
   vv, dd = daq_driver.read_analog(self.scan_task, conditions)
   dd = dd[:vv*num_sensors]
   dd = np.reshape(dd, (num_sensors, int(vv)))

To fully understand what is going on, you should check both the NI model class and the pyDAQmx documentation. Broadly
speaking, we get all the available data and we reshape it to have it organized by channel in a matrix and not
interleaved according to the acquisition order (remember that most NI cards have only one analog-to-digital and one multiplexor).

With this we have covered the basic ideas behind building your own experiment class to perform a custom-made experimen.
Of course there are many details that were left out and that have to be understood separately.

.. automodule:: experimentor.models.daq.ni6251
   :members:

.. autoclass:: experimentor.models.daq.ni6251.NI
   :members:
