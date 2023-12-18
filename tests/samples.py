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
        Out6/Block:  [ Packets: 0                  Bytes: 0                  ]"""
