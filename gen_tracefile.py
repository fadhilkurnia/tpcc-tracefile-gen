#!/usr/bin/python3

import subprocess
import json
import shutil
import os

# for each transaction in tpcc, record:
#   - transaction id: increasing number
#   - transaction type: 'payment' 'new_order' ''
#   - transaction queries: string
#   - exec time: prerecorded execution time
#   - list of diffs: 
#       - file_id
#       - address
#       - offset
#       - length

tpcc_queries_loc = 'tpcc.sql'
tpcc_database = 'tpcc.db'
tpcc_database_run = 'tpcc_run.db'
shutil.copy(tpcc_database, tpcc_database_run)
tpcc_exec_time = {'NEW_ORDER': 33958328.01, 'PAYMENT': 18908170.22, 'ORDER_STATUS': 188177.59, 'STOCK_LEVEL': 783442.97, 'DELIVERY': 3598365.55}
result_loc = 'tpcc_trace.csv'
result_file = open(result_loc, 'w')
result_file.write(f'tx_id,tx_type,queries,exec_time(us),state_diff_list\n')

def get_state_diff(tx_id, tx_type, queries):
    # run the query, and record the pwrite syscalls
    subprocess.run(f'sudo ltrace -o raw -Sf sqlite3 {tpcc_database_run} "{queries}"', shell=True)
    # gather the state diffs
    temp_raw_file = open("raw")
    filtered_lines = []
    for line in temp_raw_file:
        if "SYS_pwrite(" in line:
            filtered_lines.append(line)
    result_state_diffs = ""
    for l in filtered_lines:
        syscall_raw = l.rstrip().split(', ')
        file_id = syscall_raw[0]
        file_id = file_id[file_id.find('(')+1:]
        address = syscall_raw[1]
        length =  int(syscall_raw[2])
        # offset can be in hexadecimal
        offset =  syscall_raw[3][:syscall_raw[3].find(')')]
        if 'x' in offset:
            offset = int(offset, 16)
        else:
            offset = int(offset)
        cur_state_diff = f"file_id:{int(file_id)};address:{str(address)};length:{int(length)};offset:{int(offset)}"
        if len (result_state_diffs) > 0:
            result_state_diffs += "|"
        result_state_diffs += cur_state_diff
    
    result_file.write(f'{tx_id},"{tx_type}","{queries}",{tpcc_exec_time[tx_type]},"{result_state_diffs}"\n')
    temp_raw_file.close()

tx_type_pattern = set(['"NEW_ORDER";', '"PAYMENT";', '"ORDER_STATUS";', '"STOCK_LEVEL";', '"DELIVERY";'])
is_mode_record_transaction = False
tx_query = ""
cur_tx_type = ""
tx_id = 0
tpcc_queries_file = open(tpcc_queries_loc)
for l in tpcc_queries_file:

    if is_mode_record_transaction:
        tx_query = f"{tx_query} {l.rstrip()}"

    if l.rstrip() in tx_type_pattern:
        cur_tx_type = l.rstrip()[1:-2]
        is_mode_record_transaction = True
        print(f">> processing tx-{tx_id} {cur_tx_type}")
        continue
    
    if "COMMIT;" in l:
        is_mode_record_transaction = False
        get_state_diff(tx_id, cur_tx_type, tx_query)
        cur_tx_type = ""
        tx_query = ""
        tx_id += 1


tpcc_queries_file.close()
result_file.close()
os.remove(tpcc_database_run)