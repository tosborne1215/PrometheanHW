# Requirements:

- Please use Python language v2.7.x

- Please implement a stand-alone script that does the following:

Input:

Taking an argument “root_dir” as a root directory to start traversing.

Taking an argument “keyword” as a regular expression for example ( “^[a-zA-Z]+_TESTResult.*” ) to detect that a file contains a string

Functionality:

The script should recursively walk the “root_dir” and detect all the files under that dir contains “keywords” and count the number of files for that sub dir. All results should be saved in a key:value array with key being subdir string, and value being counts of file contains the key line

Output:

A output array of all the data, for example {’a/b’: 6, ’a/b/c’: 7, ‘/a/b/c/d’:0}

Stretch goal:- An output graph with a plot with X as subdir name string, Y as count values.

Tests: Please design a set of tests for the above routine you just wrote, how many ways can break the routine above and how many ways can you test the routine. Send these tests in a text file. 

The code will be evaluated based on the following criteria:

- Coding style - module name, class name, functions, clarity, data structure, algorithms etc.

- Argument handling - what module do you use for argument that’s easy to expend, exception checking etc.

- Portability - think about how your program would behavior for various OS systems

- Scalability - how do you make your routine scalable, multithreading, parallel computing etc.

- Reliability - how robust can you make the routine that under any environment it won’t crash - either exit gracefully with error message or complete what you can