This code is GUI-based so it requires controlling your screen.

You can run it on the main computer but you can not use the computer at the same time.

Therefore, the better plan is to create some Virtual Machines running Windows OS so the code can be implemented parallelly.

Each Virtual Machine requires at least 1 CPU Processor, 3 GB of Ram, and 50 GB of Hard Disk, and it will run one of three GUI codes, which are Meta.bat, Meta2.bat, and Meta3.bat.

The main computer with more computing resources will run the Meta_check_download.bat in the background mode (to open the bat file, just need a double click), which will process the downloaded data in the type of CSV files (about 50 GB of data per day).

All the code is scheduled to be run day by day from 9 am to 11 pm, so you only need to open and set up it only once.

Note: Metabase completes updating the data of yesterday at 9 am, so the code cannot be run before 9 am.

Note2: The Meta_check is a manually and independently check for the completion of the code.
