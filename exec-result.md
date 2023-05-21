Result of TPCC SQLite execution in m510 machine.

```
$ python3 tpcc.py --stop-on-error --no-load sqlite
[<module>:233] INFO : Initializing TPC-C benchmark using SqliteDriver
[execute:056] INFO : Executing benchmark for 60 seconds
==================================================================
Execution Results after 60 seconds
------------------------------------------------------------------
                  Executed        Time (µs)       Rate
  DELIVERY        679             3598365.55      188.70 txn/s
  NEW_ORDER       7542            33958328.01     222.10 txn/s
  ORDER_STATUS    697             188177.59       3703.95 txn/s
  PAYMENT         7133            18908170.22     377.24 txn/s
  STOCK_LEVEL     680             783442.97       867.96 txn/s
------------------------------------------------------------------
  TOTAL           16731           57436484.34     291.30 txn/s
```