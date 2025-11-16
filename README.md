# TraceR Automated Tests using The Sentinel

An automated testing framework for the TraceR robot arm using pytest and Docker.

### Overview

- Integrating this to a CICD pipeline, a dedicated robot arm TraceR will be used as the automation agent.
- For any system update available, TraceR will then be triggered to upgrade followed by the execution of the validation program Sentinel.
- Sentinel performs the standard ***Feed → Digest → Verify*** sequence on every test input it provides to TraceR and generates a Pass/Fail report.
- By default, Sentinel uses predefined test inputs to validate TraceR, but it can also generate random inputs for reliability and performance testing.

<img width="1825" height="579" alt="image" src="https://github.com/user-attachments/assets/fb2f6bf4-e453-411d-95f5-92b96cae6c76" />
