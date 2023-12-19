sample_info_output = """Status: Enabled for 25 days 16:23:32          Debug: Urgent

Hostid:   0x68d01842
Checksum: 0x1d921dc03c175342eebc265ff2573361

State Table                          Total             Rate
  current entries                        2               
  searches                         5165885            2.3/s
  inserts                            94115            0.0/s
  removals                           94113            0.0/s
Source Tracking Table
  current entries                        0               
  searches                               0            0.0/s
  inserts                                0            0.0/s
  removals                               0            0.0/s
Counters
  match                            3177960            1.4/s
  bad-offset                             0            0.0/s
  fragment                               0            0.0/s
  short                                  0            0.0/s
  normalize                              0            0.0/s
  memory                                 0            0.0/s
  bad-timestamp                          0            0.0/s
  congestion                             0            0.0/s
  ip-option                              0            0.0/s
  proto-cksum                            0            0.0/s
  state-mismatch                         0            0.0/s
  state-insert                           0            0.0/s
  state-limit                            0            0.0/s
  src-limit                              0            0.0/s
  synproxy                               0            0.0/s
  map-failed                             0            0.0/s
Limit Counters
  max states per rule                    0            0.0/s
  max-src-states                         0            0.0/s
  max-src-nodes                          0            0.0/s
  max-src-conn                           0            0.0/s
  max-src-conn-rate                      0            0.0/s
  overload table insertion               0            0.0/s
  overload flush states                  0            0.0/s
  synfloods detected                     0            0.0/s
  syncookies sent                        0            0.0/s
  syncookies validated                   0            0.0/s
Syncookies
  mode                      never
  active                    inactive
  highwater                 25 %
  lowwater                  12 %
  halfopen states           0
"""

sample_interfaces_output = """all
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  0                 
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In6/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
bridge
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  0                 
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In6/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
bridge3
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  0                 
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 802102             Bytes: 137417498          ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 30                 Bytes: 1720               ]
	In6/Block:   [ Packets: 696051             Bytes: 146163850          ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
em0.3
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  27                
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 802104             Bytes: 137417878          ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 40                 Bytes: 2320               ]
	In6/Block:   [ Packets: 696043             Bytes: 146163670          ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
em0.4
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  27                
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 184339             Bytes: 29172941           ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 2938               Bytes: 163008             ]
	In6/Block:   [ Packets: 43643              Bytes: 6389105            ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
em0.7
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  28                
	In4/Pass:    [ Packets: 881102             Bytes: 262038497          ]
	In4/Block:   [ Packets: 24                 Bytes: 1440               ]
	Out4/Pass:   [ Packets: 1313278            Bytes: 905857458          ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In6/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
lo0 (skip)
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  0                 
	In4/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In4/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out4/Block:  [ Packets: 0                  Bytes: 0                  ]
	In6/Pass:    [ Packets: 0                  Bytes: 0                  ]
	In6/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Pass:   [ Packets: 0                  Bytes: 0                  ]
	Out6/Block:  [ Packets: 0                  Bytes: 0                  ]
"""

sample_rules_output = """scrub in on em0.3 all fragment reassemble
  [ Evaluations: 369261    Packets: 30116     Bytes: 0           States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
scrub in on em0.4 all fragment reassemble
  [ Evaluations: 339145    Packets: 10460     Bytes: 0           States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
scrub in on em0.7 all fragment reassemble
  [ Evaluations: 328685    Packets: 117821    Bytes: 17766261    States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
scrub in on epair1a all fragment reassemble
  [ Evaluations: 59092     Packets: 0         Bytes: 0           States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
block drop log all
  [ Evaluations: 88951     Packets: 81079     Bytes: 15024708    States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
pass in quick on em0.3 inet6 proto ipv6-icmp all icmp6-type echoreq keep state
  [ Evaluations: 88951     Packets: 0         Bytes: 0           States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
pass in quick on em0.7 proto tcp from <prometheus6> to <nuc2> port = 9999 flags S/SA keep state
  [ Evaluations: 81079     Packets: 42615     Bytes: 33758359    States: 1     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
pass in quick proto tcp from <allowssh> to <firewalls_own_ips> port = ssh flags S/SA keep state
  [ Evaluations: 81079     Packets: 0         Bytes: 0           States: 0     ]
  [ Inserted: uid 0 pid 2786 State Creations: 0     ]
"""

sample_tables_output = """--a-r--	allowssh
	Addresses:   12
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  [ Anchors: 0                  Rules: 2                  ]
	Evaluations: [ NoMatch: 550                Match: 0                  ]
	In/Block:    [ Packets: 0                  Bytes: 0                  ]
	In/Pass:     [ Packets: 0                  Bytes: 0                  ]
	In/XPass:    [ Packets: 0                  Bytes: 0                  ]
	Out/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out/Pass:    [ Packets: 0                  Bytes: 0                  ]
	Out/XPass:   [ Packets: 0                  Bytes: 0                  ]
--a-r--	nuc2
	Addresses:   1
	Cleared:     Fri Dec  1 11:02:46 2023
	References:  [ Anchors: 0                  Rules: 2                  ]
	Evaluations: [ NoMatch: 0                  Match: 25                 ]
	In/Block:    [ Packets: 0                  Bytes: 0                  ]
	In/Pass:     [ Packets: 461268             Bytes: 57925850           ]
	In/XPass:    [ Packets: 0                  Bytes: 0                  ]
	Out/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out/Pass:    [ Packets: 661462             Bytes: 830514949          ]
	Out/XPass:   [ Packets: 0                  Bytes: 0                  ]
-pa----	portknock
	Addresses:   0
	Cleared:     Sun Nov 19 18:50:41 2023
	References:  [ Anchors: 0                  Rules: 0                  ]
	Evaluations: [ NoMatch: 0                  Match: 0                  ]
	In/Block:    [ Packets: 0                  Bytes: 0                  ]
	In/Pass:     [ Packets: 0                  Bytes: 0                  ]
	In/XPass:    [ Packets: 0                  Bytes: 0                  ]
	Out/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out/Pass:    [ Packets: 0                  Bytes: 0                  ]
	Out/XPass:   [ Packets: 0                  Bytes: 0                  ]
--a-r--	prometheus6
	Addresses:   1
	Cleared:     Fri Dec  1 11:07:06 2023
	References:  [ Anchors: 0                  Rules: 2                  ]
	Evaluations: [ NoMatch: 0                  Match: 25                 ]
	In/Block:    [ Packets: 0                  Bytes: 0                  ]
	In/Pass:     [ Packets: 461268             Bytes: 57925850           ]
	In/XPass:    [ Packets: 0                  Bytes: 0                  ]
	Out/Block:   [ Packets: 0                  Bytes: 0                  ]
	Out/Pass:    [ Packets: 661462             Bytes: 830514949          ]
	Out/XPass:   [ Packets: 0                  Bytes: 0                  ]
"""
