# TPCC Tracefile Generator

The main code (`gen_tracefile.py`) iterate through all the TPCC queries in `tpcc.sql` that are generated via [py-tpcc](https://github.com/apavlo/py-tpcc/).
For each query, the code execute it on sqlite while recording `pwrite` syscall in the background using `ltrace` to capture all the state diffs after each transaction execution.
The state diffs consist of the address, offset, and length of the updated state in the file system.

An example of the resulting tracefile can be accessed at [tpcc_trace.csv](./tpcc_trace.csv) file.

Due to Github storage limitation, we put the actual database (`tpcc.db`), queries (`tpcc.sql`), and the complete resulting tracefile (`tpcc_trace.csv`) in this [drive folder](https://drive.google.com/drive/folders/1xP89k1MlsWrVFaF_bIkGZcT0kA1bqSGF?usp=sharing).