# SLS_RECON
Reads data from and creates tif file of each elemenet detected.
Will use the "dead time corrected values" when they are recorded.
The sum of values recorded by each detector is used.
Pixels with no value recorded are assigned NAN (numpy.NAN)
A .log file is also created. This file contains the size of the pixels.

OPEN IMAGES IN FIJI TO ADJUST CONTRAST etc

Tested in unix with python 2.7.3

Needs numpy and PIL.

Example call:
$python read_sls.py "/path/to/sls_data.txt"

