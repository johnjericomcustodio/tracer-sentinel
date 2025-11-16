# TraceR Automated Tests using The Sentinel

An automated testing framework for the TraceR robot arm using pytest and Docker.

### How does this work?

1. The Sentinel program supplies a *system_input_file.txt* to TraceR using the required format:

```bash
Rectangle
(-4, -150), (-4, 150), (160, -150), (160, 150)
Points
(-3, -149)
(4, 150)
(170, 150)
(150, -155)
(-6, 160)
(-4,-150)
(-4.23, -150.56)
(0.045, 0.001)
```
2. TraceR takes the expected visit points from the input file listed under keyword *Points*
3. TraceR visits points one by one only within the work area defined by the coordinates under the keyword *Rectangle*.
4. TraceR provides the list of actual visited points by writing them in an output file *system_output_file.txt* with the following format:

```bash
(-3, -149)
(4, 150)
(170, 150)
(0,0)
error
(150, -155)
(-6, 160)
(-4,-150)
(4, 150)
(-4.23, -150.56)
(160.00, -150.00)
()
```
5. Sentinel digests both the input and output files to verify correctness and compare expected vs. actual visited points.
6. Sentinel determines whether TraceR successfully visited all required points and produces a PASS/FAIL result in *test_results.txt*, along with a plotted image showing the rectangle and all points.
   
<img width="1103" height="617" alt="image" src="https://github.com/user-attachments/assets/af64f655-7eb2-4bbc-82db-1e58e1d568c5" />

### Potential Architecture for CICD

<img width="1825" height="579" alt="image" src="https://github.com/user-attachments/assets/fb2f6bf4-e453-411d-95f5-92b96cae6c76" />

- Integrating this to a CICD pipeline, a dedicated robot arm TraceR will be used as the automation agent.
- For any system update available, TraceR will then be triggered to upgrade/downgrade followed by the execution of the validation program Sentinel.
- Sentinel performs the standard ***Feed → Digest → Verify*** sequence on every test input it provides to TraceR and generates a Pass/Fail report.
- A plot will also be generated to visualize TraceR's work area and map the actual versus expected visit points.
- By default, Sentinel uses predefined test inputs to validate TraceR, but it can also generate random inputs for reliability and performance testing.






