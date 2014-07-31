Title: CLA-query
Author: Thomas Hodgson
Date: 31 July 2014

This script searches the [Copyright Licensing Agency's](http://www.cla.co.uk) database for permissions. The script is written in Python and tested using version 3.4.1 on OSX Mavericks. Note that I'm not affiliated with the CLA, although I did ask them before making this code public. I'd like to thank the people I spoke to for their help. They can be contacted about their API at <api@cla.co.uk>.

# Usage

The script can be run from the command line as follows

```
$ python3 cla.py [--LicenceType, -L {132,134,136,137,140,141,143,154,230,232}] [--UsageType, -U {1,2,8}] [--ISBNname, -I ISBN_NAME] [--key, -K KEY] <file>
```

Defaults have been set for the named arguments: 132 (a Higher Education licence), 2 (scanning), 'ISBN', and 'key.txt', respectively.

# What it does

The script looks at the file given as an argument, which must be an Excel file with extension '.xlsx' or '.xls'. (The script will find a file with the name given if no extension is specified and one with a suitable extension exists.) The first worksheet in the workbook is inspected for a column header that matches the ISBNname argument. The entries in that column are used to query the CLA's database. A key is read from the key argument; in order to use the script you will need to obtain a key from the CLA. The responses from the database are written to a column called 'Responses' in a new Excel file based on the following mapping:

* NegativeHeader -> 'Negative'
* NeutralHeader -> 'Neutral'
* PositiveHeader -> 'Positive'
* WarningHeader -> 'Warning'

The new file will have the name of the original with the date (in ISO format) appended. A log file called 'cla.log' will be written containing full details of the requests sent and responses received. This is overwritten by each new call to the script.

# Requirements

The script uses some modules that are not part of the standard Python 3 installation.

* [Openpyxl](https://pythonhosted.org/openpyxl/) (tested with version 2.0.4)
* [Requests](http://docs.python-requests.org/en/latest/) (tested with version 2.3.0)

# Licence

The MIT License (MIT)

Copyright (c) 2014 Thomas Hodgson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
