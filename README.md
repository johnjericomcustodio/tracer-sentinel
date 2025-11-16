# TraceR Automated Tests using The Sentinel

An automated testing framework for the TraceR robot arm using pytest and Docker.

### Overview

<img width="1825" height="579" alt="image" src="https://github.com/user-attachments/assets/fb2f6bf4-e453-411d-95f5-92b96cae6c76" />

- Integrating this to a CICD pipeline, a dedicated robot arm TraceR will be used as the automation agent.
- For any system update available, TraceR will then be triggered to upgrade/downgrade followed by the execution of the validation program Sentinel.
- Sentinel performs the standard ***Feed → Digest → Verify*** sequence on every test input it provides to TraceR and generates a Pass/Fail report.
- A plot will also be generated to visualize TraceR's work area and map the actual versus expected visit points.
- By default, Sentinel uses predefined test inputs to validate TraceR, but it can also generate random inputs for reliability and performance testing.

<img width="1103" height="617" alt="image" src="https://github.com/user-attachments/assets/af64f655-7eb2-4bbc-82db-1e58e1d568c5" />




