<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/johnjericomcustodio/tracer-sentinel/">
    <img src="images/logo_sentinel.png" alt="Logo" width="800" height="800">
  </a>
  <h3 align="center">Sentinel - The Automated Test Framework for Robot Arm TraceR</h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#operation-flow">Operation Flow</a></li> 
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#cicd">CICD</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>

## About The Project

### Built With

### Operation flow

1. The Sentinel program supplies a *system_input_file.txt* to TraceR using the required format:

```bash
Rectangle
(11.01, 4.69), (6.84, 8.1), (5.41, 6.35), (9.59, 2.94)
Points
(8.34, 6.61)
(7.66, 5.6)
(5.69, 6.13)
```
2. TraceR takes the expected visit points from the input file listed under keyword *Points*
3. TraceR visits points one by one only within the work area defined by the coordinates under the keyword *Rectangle*.
4. TraceR provides the list of actual visited points by writing them in an output file *system_output_file.txt* with the following format:

```bash
(1.5, 3.1)
(6.2, 2.8)
(4.5, 3.2)
```
5. Sentinel digests both the input and output files to verify correctness and compare expected vs. actual visited points.
6. Sentinel determines whether TraceR successfully visited all required points and produces a PASS/FAIL result in *test_results.txt*, along with a plotted image showing the rectangle and all points.

<a href="https://github.com/johnjericomcustodio/tracer-sentinel/">
  <img src="images/workarea_points.png" width="1562" height="756">
</a>

## Getting Started

### Prerequisites

### Installation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## CICD

<a href="https://github.com/johnjericomcustodio/tracer-sentinel/">
  <img src="images/tracer_sentinel_cicdarch.png" width="1825" height="579">
</a>

- Integrating this to a CICD pipeline, a dedicated robot arm TraceR will be used as the automation agent.
- For any system update available, TraceR will then be triggered to upgrade/downgrade followed by the execution of the validation program Sentinel.
- Sentinel performs the standard ***Feed → Digest → Verify*** sequence on every test input it provides to TraceR and generates a Pass/Fail report.
- A plot will also be generated to visualize TraceR's work area and map the actual versus expected visit points.
- By default, Sentinel uses predefined test inputs to validate TraceR, but it can also generate random inputs for reliability and performance testing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## References

- [README template](https://github.com/othneildrew/Best-README-Template/blob/main/README.md)
- [Markdown Guide - Basic Syntax](https://www.markdownguide.org/basic-syntax/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
