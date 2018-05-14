# Overview

The requirements have been pasted below. There are a number of assumptions I've had to make about the project. I believe the requirements are designed to be difficult to meet. Additionaly meeting all the requirements does not seem possible within a reasonable amount of time. Naive solutions could be created that do not meet most of the requirements.

The sections following requirements will detail my initial approach, tests, edge cases, and assumptions (not in that order).

What is included in this zip?

- This readme!
- app_test.py which contains various unittests
- app.py the application itself. I probably should think about a new name.

## Requirements:

- Please use Python language v2.7.x

- Please implement a stand-alone script that does the following:

### Input:

Taking an argument “root_dir” as a root directory to start traversing.

Taking an argument “keyword” as a regular expression for example `“^[a-zA-Z]+_TESTResult.*”` to detect that a file contains a string

### Functionality:

The script should recursively walk the “root_dir” and detect all the files under that dir contains “keywords” and count the number of files for that sub dir. All results should be saved in a key:value array with key being subdir string, and value being counts of file contains the key line

### Output

A output array of all the data, for example {’a/b’: 6, ’a/b/c’: 7, ‘/a/b/c/d’:0}

### Stretch goal

An output graph with a plot with X as subdir name string, Y as count values.

### Tests

Please design a set of tests for the above routine you just wrote, how many ways can break the routine above and how many ways can you test the routine. Send these tests in a text file. 

### Evalutation
The code will be evaluated based on the following criteria:

- Coding style - module name, class name, functions, clarity, data structure, algorithms etc.

- Argument handling - what module do you use for argument that’s easy to expend, exception checking etc.

- Portability - think about how your program would behavior for various OS systems

- Scalability - how do you make your routine scalable, multithreading, parallel computing etc.

- Reliability - how robust can you make the routine that under any environment it won’t crash - either exit gracefully with error message or complete what you can

## Initial Approach

Use mmap to iterate over a buffer and find matches within that buffer. Subprocess can be created to look at directories or files and that can make it a bit more scalable. It may make part of it less reliable, but I believe with some reliability checks I can cover those cases adequately. mmap and subprocess do present obstacles for portability and I may need to do some OS checks and change the behavior slightly to overcome those challenges.

Build a Queue that has the files that need processed. Queues are threadsafe and I should be able to spin up as many threads to process the data as I need. I'll add the data to a stack and after all the files are processed I can then build the dict I need to return the data in.

## Assumptions/Caveats

### Immediate Concerns

Since I am receiving a regular expression my ability to ensure 100% coverage of the files using regular expression will be limited.

### File sizes are not bounded

Some files will be larger than I can load into memory. mmap is good solution to this problem, but if the regular expression match is larger than my buffer then I will not find those matches. Further a file may not have any lines and be extremely large.

### Regular expressions complexity

Without knowing what kind of regular expressions will be used I may be very limited in what I am searching for.

What if the regular expression contains an anchor and expects me to find values at the end of a line? I am searching a buffer and wont have the expected anchor or start. I could attempt to disect the regular expression but from my experience that seems destined to fail. They can be very complex.

Assumption: The pattern doesnt contain anchors

### CPU Architecture (x86 or x64 ?)

In this day and age I hope that we are running on 64-bit OS. My code is written with this in mind and there may be performance degradation if this is not the case. It will also make it more difficult to get to an IO bound solution on x86. To support x86 I would suggest a separate approach that is specific to that architecture.

Assumption: x64

### IO bound vs CPU Bound

I would consider an IO bound solution a win. I am looking at many files and an IO bound solution is a hardware limitation. There is only so much I can do to solve this. A CPU bound solution may be the fault of my software and so I am going to aim for an IO bounded solution. My dev environment has a SSD so it may be difficult to hit the IO Bound goal.

## Tests

Developing all of these tests will be a pain so my goal will be to create a 'master' TestCase that can be inheritted and it will include setUp and tearDown functions that will build very large tests and each inherrited class can point to a specific root position. This reduces the amount of time I will spend creating tests. The other issue I will encounter in my tests is finding suitable regular expressions. I think I am going to use a lorem ipsum generator to create large amounts of data to work with. I can include a list of keywords that I want to count and randomly place them in the text.

- Simple Test
- High Recursion Depth
- Too High Recursion Depth
- Long Line Test
- Huge File Test
- Huge File Single Line Test
- Long Short Line Test
- Many Subdirs test
- Many Subdirs with large files
- Invalid Input
- Out of memory exceptions

## Misc Notes
