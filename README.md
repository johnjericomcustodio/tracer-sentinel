<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/johnjericomcustodio/tracer-sentinel/">
    <img src="images/logo_sentinel.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">TraceR Automated Tests via Sentinel</h3>

  <p align="center">
    An automated testing framework for the TraceR robot arm using pytest and Docker.
  </p>
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
(6.78, 0.39), (10.42, 0.39), (10.42, 5.18), (6.78, 5.18)
Points
(7.55, 2.07)
(6.78, 3.64)
(7.06, 2.63)
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
   
<img width="1558" height="733" alt="image" src="https://github.com/user-attachments/assets/9bf91398-66ec-4656-aa60-dafa92f93013" />

## Getting Started

### Prerequisites

### Installation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## CICD

<img width="1825" height="579" alt="image" src="https://github.com/user-attachments/assets/fb2f6bf4-e453-411d-95f5-92b96cae6c76" />

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
