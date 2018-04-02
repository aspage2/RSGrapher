# RSGrapher
> "Bringing you quality hardware and software solutions... Eventually." - PNP Technologies Ltd.

## Running
Windows users should be able to double-click "run.pyw". RSGrapher can be initiated on the command line with:

    python run.pyw

### Requirements
Requires Python 3.5 or later to run. Install necessary modules with the command:

    python -m pip install -r requirements.txt

## Abstract
RSGrapher is an application meant to streamline the analysis and reporting of rebar stress data.
A **test** consists of pulling multiple samples of rebar with a massive machine to the point of
failure. During testing, the **time**, **strain** (displacement) and **stress** (load) are recorded in ~.2 second intervals.
The resulting data is returned as a text file, which RSGrapher parses into its internal data structure.

The main purpose of RSGrapher is to scale, shift and analyze this data to produce three graphs that describe several significant characteristics of the sample:
* **Peak Load**: The maximum load handled by the sample. The **Ultimate Tensile Strength** (UTS) is proportional to the peakload, represented in units of stress (PSI/KSI).
* **Yield Load**: The "yield point" of the sample; the point where the material loses elasticity and begins deforming plastically. The **Yield Strength** is proportional to the yield load, again represented in units of stress (PSI/KSI).

The three graphs output by the software are as follows:
1. Peak Load (Load (lbs) vs. Displacement (in))
2. UTS/Yield Strength (Stress (PSI) vs. Strain (% Length)
3. Yield Load (Stress (PSI) vs. Displacement (in))

The graphs are output as PDF documents formatted to the style of the final test report, with date, sample number, titles and logo.
