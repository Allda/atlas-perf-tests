## Report 2024-09-03

This report was generated using `make` command on 2024-09-03.

> **_NOTE:_**  All the values in the table bellow represents a response time
of the requests from client to Atlas and back. The X axes of the table represents
a individual buckets.


| Type   | Name                                                                          |  50%  |  66%  |  75%  |  80%  |  90%  |  95%  |  98%  |  99%  | 99.9% | 99.99% | 100% | # reqs |
|--------|-------------------------------------------------------------------------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|-------|-------|
| DELETE | /api/v1/sbom                                                                  |   260 |   280 |   310 |   320 |   390 |   460 |   680 |   740 |   740 |    740 |   740 |    76 |
| PUT    | /api/v1/sbom                                                                  |   390 |   480 |   520 |   540 |   590 |   690 |   740 |   760 |   760 |    760 |   760 |    77 |
| GET    | /api/v1/sbom/search?q=perf-test-container-1.3                                 |   190 |   200 |   210 |   230 |   340 |   380 |   400 |   400 |   400 |    400 |   400 |    75 |
| GET    | /api/v1/sbom?id=perf-test-container-1.3                                       |   610 |   660 |   720 |   740 |   900 |   980 |  1100 |  1100 |  1100 |   1100 |  1100 |    77 |
| GET    | /api/v1/vex/search?q=CVE-1990-1111                                            |   120 |   130 |   140 |   150 |   350 |   350 |   440 |   490 |   680 |    680 |   680 |   135 |
| GET    | /api/v1/vex?advisory=CVE-1990-1111                                            |   360 |   460 |   520 |   550 |   730 |   790 |   880 |   880 |   990 |    990 |   990 |   135 |
|        | Aggregated                                                                    |   320 |   380 |   470 |   520 |   650 |   740 |   880 |   970 |  1100 |   1100 |  1100 |   575 |
