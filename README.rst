To ensure up-to-date documentation, see home.uchicago.edu/~asippel/projects/p2acnet.html

.. _p2acnet:

---------------------
Python 2 ACNET Module
---------------------

Description
-----------

This module interfaces with datalogger information on Fermilab's ACNET. The program allows one to send data requests to
ACNET of specified channels/times. It then parses the data, and can either return it in a dictionary of channel:data_array
pairs or plot the results with a formatted x-axis.

.. note::

	In order to access the data and make use of this module, one must be connected to the Fermilab network either onsite
	or via VPN.

How It Works
------------

There are two classes in the module, the P2ACNET class and P2ACNETSingle class. The P2ACNETSingle class handles single channel queries
and either returns a data array or makes a plot of the single channel data. The P2ACNET class is like a factory of the
P2ACNETSingle class, creating new instances for each channel in a supplied channel list. Most user interaction will be with the 
P2ACNET class, which in fact can handle single channel queries by passing them either as a string or a single element list.

The module makes use of the requests Python package to send  HTTP requests to ACNET.
(see information at `Requests Main Page <http://docs.python-requests.org/en/latest/>`_)

The queries this module sends to ACNET make use of Fermilab's ACL scripting language for communicating with accelerator control
devices. (more information can be found at `ACL Scripting Intro <http://www-ad.fnal.gov/help/ul_clib/intro_acl.html>`_)

How to Use
----------

Necessary Packages
~~~~~~~~~~~~~~~~~~

This module makes use of the following packages, each of which need to be installed in order for it to run correctly:

* Requests: `Online Documentation <http://docs.python-requests.org/en/latest/>`_
* Numpy
* Matplotlib
* Datetime (built-in Python module as of version 2.3)
* Collections (built-in Python module as of version 2.4)

Getting Started
~~~~~~~~~~~~~~~

**Obtaining the Files**

There exists a git repository for anyone with ssh access to dorothy at dorothy.fnal.gov/git/p2acnet/

One can clone this repository by entering the following in the terminal::

	git clone username@dorothy.fnal.gov:/git/p2acnet

I have also made a repository on GitHub for those who don't have access to cmbpol. Simply clone from git@github.com:asippel89/p2acnet.git::

  git clone git@github.com:asippel89/p2acnet.git


**Using the Module**

The only necessary file is p2acnet.py. Place this in your working directory. The module can be run as a script by editing the content below::

	if __name__ == '__main__':

to suit your needs and then running python p2acnet.py from the command line. Alternatively, it can be imported and used in a separate script by instantiating the relevant classes (see examples below).

**Required Input**

The P2ACNET class requires a list of channel names and start and end times as input. The start/end times must be formatted as
'DD-MON-YEAR-HH:MM', where month is the allcaps abbreviation and HH:MM is in military time. So, if you would like to input a start date/time 
of Oct. 3, 2012 at 5:30 PM::

	time = '03-OCT-2012-17:30'

Other acceptable time entries include 'Yesterday', 'Today', 'Now'.

Examples
~~~~~~~~

**Import and use in separate script, Make a plot of 4 channels**::

	import p2acnet
	
	channel_list = ['E:TCIP', 'E:TNIP0', 'E:TNIP1', 'E:TNESIP']
	start_time = '20-OCT-2012-05:00'
	end_time = '23-OCT-2012-17:00'
	query = p2acnet.P2ACNET(channel_list, start_time, end_time)
	plot = query.plot_group('T IFO North Arm Response to Power Outage')

This results in the following plot:

.. image:: /images/T-IFO-N-Arm-Power-Outage.png
	:alt: p2acnet example 1
	:height: 400px
	:width: 600px

**Plot list of channels whose units aren't all the same**::

	import p2acnet

	units_test_list = ['E:TCIP', 'E:TNIP0', 'E:TNIP1', 'E:TNESIP', 'E:TEIP0', 'E:TEIP1', 'E:TEESIP', 'G:OUTTMP', 'G:WCHILL']
	start_time = '24-OCT-2012-17:30'
	end_time = '26-OCT-2012-18:00'
	query = p2acnet.P2ACNET(units_test_list, start_time, end_time)
	plot = query.plot_group('T IFO and Outside Temp/Wind Chill')

Resulting plot:

.. image:: /images/T-IFO-and-Outside-Temp.png
	:alt: p2acnet example 2
	:height: 500px
	:width: 600px

.. note::
   
   One can also specify plot labels that will show up in the legend of the plot. This is done by setting the channel parameter to 'CHANNEL=LABEL'. So, in the above example if we wanted the temperature label (currently G:OUTTMP) to be different, we would change the units_test_list to be::

     units_test_list = ['E:TCIP', 'E:TNIP0', 'E:TNIP1', 'E:TNESIP', 'E:TEIP0', 'E:TEIP1', 'E:TEESIP', 'G:OUTTMP=Outside Temp', 'G:WCHILL']

**Get response data using get_group_data() method**::

	import p2acnet

	channel_list = ['E:HADC01', 'E:HADC02', 'E:HADC03']
	start_time = '24-OCT-2012-17:30'
	end_time = '26-OCT-2012-18:00'
	query = p2acnet.P2ACNET(channel_list, start_time, end_time)
	data = query.get_group_data()	

The get_group_data() method of the P2ACNET class returns a dictionary whose keys are the individual channels and whose values
are the returned data arrays for that channel. The shape of the data array is 2 columns (datetime element and value) and N rows 
(the number of logged data values for that time frame and channel). To work with the response data, one could (continuing the example above)::

  EHADC01_data = data['E:HADC01']
  EHADC01_data

yields::
  
  array([[2012-10-24 17:30:00.733000, 1.356],
    [2012-10-24 17:30:01.732000, 1.356],
    [2012-10-24 17:30:02.732000, 1.355],
    ..., 
    [2012-10-26 17:59:57.513000, 1.356],
    [2012-10-26 17:59:58.513000, 1.357],
    [2012-10-26 17:59:59.512000, 1.356]], dtype=object)

The datetime entries in the array (1st column) are normal python datetime objects, and the 2nd column are the returned data values.
	
Holometer-Relevant Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below is a list of Holometer-relevant ACNET channels and a short description:

**T Interferometer**

==============  ===========================  ==========  =================
Channel Name          Description              Units       Log Frequency
==============  ===========================  ==========  =================
E:TCIP           TCIP T IFO Central IP          Torr            1 Hz
E:TNIP0          TNIP0 T IFO northarm IP0       Torr            1 Hz
E:TNIP1		 TNIP1 T IFO northarm IP1	Torr		1 Hz	
E:TNESIP	 TNESIP T IFO north cube	Torr		1 Hz
E:TEIP0		 TEIP0 T IFO east IP0		Torr		1 Hz
E:TEIP1		 TEIP1 T IFO east IP1		Torr		1 Hz
E:TEESIP	 TEESIP T IFO east cube		Torr		1 Hz
==============  ===========================  ==========  =================

**L Interferometer**

==============  ===========================  ==========  =================
Channel Name          Description              Units       Log Frequency
==============  ===========================  ==========  =================
E:LCIP           LCIP L IFO Central IP          Torr            1 Hz
E:LNIP0          LNIP0 L IFO northarm IP0       Torr            1 Hz
E:LNIP1		 LNIP1 L IFO northarm IP1	Torr		1 Hz	
E:LNESIP	 LNESIP L IFO north cube	Torr		1 Hz
E:LEIP0		 LEIP0 L IFO east IP0		Torr		1 Hz
E:LEIP1		 LEIP1 L IFO east IP1		Torr		1 Hz
E:LEESIP	 EESIP L IFO east cube		Torr		1 Hz
==============  ===========================  ==========  =================

**Laser Monitoring**

===========================  ==================================================
 ACNET: Channel Name          Description  
===========================  ==================================================
E:HADC01    0-10V ADC CH 1    Diode laser 1, power monitor, 1 V/W
E:HADC02    0-10V ADC CH 2    Diode laser 2, power monitor, 1 V/W
E:HADC03    0-10V ADC CH 3    Laser crystal, TEC error signal, 10 V/degC
E:HADC04    0-10V ADC CH 4    Diode laser 1, TEC error signal, 10 V/degC
E:HADC05    0-10V ADC CH 5    Diode laser 2, TEC error signal, 10 V/degC
E:HADC06    0-10V ADC CH 6    Diode laser 1, temperature guard
E:HADC07    0-10V ADC CH 7    Diode laser 2, temperature guard
E:HADC08    0-10V ADC CH 8    Noise Eater, monitor
E:HADC09    0-10V ADC CH 9    Interlock (on ACNET module 2nd from left, top)
===========================  ==================================================


Future Directions
-----------------

Below is a list of items that will be implemented in future releases:

* Added logic to prevent slowdown for huge response sizes (use decimation)
* Included Holometer-relevant methods
* More readable x-axis for plots (use major and minor ticks)
* Ability to pass arguments and run from command line as an executable script
* Upload this script to pypy (?) and make it installable via easy_install or pip install

Development
-----------

This section will be updated as development is being done. Major updates will be have their own subsections describing the changes.

Tuesday Nov. 27, 2012
~~~~~~~~~~~~~~~~~~~~~

Proposal to change the naming scheme and hierarchy of the p2acnet module:

* Clean up current code

  - Change the way the error handling is done ("It is better to ask forgiveness...")
  - Set up to allow extraneous http requests to be passed (better implementation than the speed mode)
* Turn p2acnet into a package with separate modules for different functions related to accessing data from ACNET

  - Logger functionality: Access an ACNET logger for a range of values for certain channels

    * Plot the results
    * Return the data
  - Instantaneous value access: get the instantaneous value of certain channels
  - Long-Connection functionality: access/log instantaneous values

    * Continuously plot the data
    * Log the values, build data sets
    * Create a warning system that analyzes data and can notify user if outside certain range (seems Holometer specific)
* Create GUI for p2acnet that can implement each of these new features

Tuesday Oct. 23, 2012
~~~~~~~~~~~~~~~~~~~~~

Used the following url as the request_info query: `<http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=show+e:hadc02/text/units/FTD>`_

Monday Oct. 22, 2012
~~~~~~~~~~~~~~~~~~~~

Read more about the ACL scripting language and making multi-line script queries via HTTP. For example, the following url shows a list of channels, their current values,\
  and their units.: `<http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=device_list/create+devs+devices=\'E:TCIP,E:TNIP0,E:TNIP1,E:TNESIP\';read_list+device_list=devs>`_

See the ACL Scripting link above for more information. Specifically, look at the read_list, read, and list commands.

Under logger_get command, can see many options. Of particular note are the max_entries={n} option and units option.

Thursday Oct. 18, 2012
~~~~~~~~~~~~~~~~~~~~~~

Now able to successfully query a list of channels and start, end time and either a dictionary of channel -> np.array or a plot with formatted dates on x-axis!

Things to work on now to clean up the code:

- Clean up/test parser to avoid errors; it seems that the value response sometimes has fewer than 2 spaces before the value
- Clean up plot_group implementation to be consistent with the rest of the group class 
- Write in some logic regarding the query response size which smartly handles huge data responses when storipng, plotting (will need to do benchmarking)
- Add the functionality for the plotter which knows the channel units and adds coordinated subplots
- See if I can add major/minor ticks for ease of understanding the returned plots
- Write docstrings!! Also consult Lee/references for best practices!

Future directions:

- Make a Kron-Job (?) in linux which runs a sweet of queries and saves the plots in a dedicated directory
- Make program executable from the command line by using ARG_PARSE within python
- Consider making the plot update in realtime
- Consider making a gui with gtk/others
- Consider putting program on a website using cgi-equivalent methods (look up AJAX?)


Tuesday Oct. 16, 2012
~~~~~~~~~~~~~~~~~~~~~

* Discovered that the performance issues were not significantly improved by switching to using iter_lines() instead of loading the entire content\
    of the HTTP response into memory. The lag was caused by including the::
	
	self.data_array = np.array(data_list)

    in the parse_query() loop, thereby recreating a numpy array with every iteration.
* Wrote a test module for 2 different p2acnet modules which takes a list of constructors and runs the parse_query() method (which is common to\
   them both), comparing the time it takes them to finish.

  - Constructors are a special type of function which generate class instances (Need to look up more info about them)
  - Could expand the test module to output more test parameters or run through different types of data

Friday Oct. 12, 2012
~~~~~~~~~~~~~~~~~~~~

* Using requests, able to successfully query ACNET while on the Fermilab network
* Proceeded with successfully parsing the output, with a python datetime object in the first element of each row, and a floating point number in the second
* Attempted plotting the data array and testing the datetime object, but came to an error on dorothy which I suspect is due to outdated matplotlib files
* Seems to work when using a test query on one of the channels that log every second over a 5 minute period, though when I change it to a month period, the output changes to 'ValueError: Unconverted data remains'

  - Consider using iter_lines or iter_content from requests for handling large data sets 

Other Information
-----------------

* There exists a Matlab interface to get the logger data from ACNET (see `Simple Matlab D 44 <http://www-bd.fnal.gov/issues/wiki/SimpleMatlabD44>`_).
* I ended up searching through endless Accelerator Control documents until I found the document which explains Fermilab's
  special scripting language ACL. (`ACL Scripting <http://www-ad.fnal.gov/help/ul_clib/intro_acl.html>`_)

* The following url brings up the data queried with time and value pairs: 
  `<http://www-ad.fnal.gov/cgi-bin/acl.pl?acl=logger_get/double/node=fastest/start=11-OCT-2012-12:30/end=11-OCT-2012-12:35+E:HADC02>`_
 
  - Note that the above url will only work from within the Fermilab network.

* Node is the Logger being queried. I found 'fastest' to work fine for the above channel, possibly need to consult ACL Scripting
  for more accurate values given a specific channel. 
