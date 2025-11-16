# tracer-sentinel
CI/CD-integrated automated testing framework for the TraceR robot arm. On system updates, the pipeline triggers TraceR and runs the Sentinel validation engine. Sentinel performs a Feed → Digest → Verify sequence, comparing expected vs. actual results and generating PASS/FAIL reports. Supports predefined and random inputs
