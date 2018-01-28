# RSGrapher
> "Bringing you quality hardware and software solutions... Eventually." - PNP Technologies Ltd.

## Running
Windows users should be able to double-click "run.pyw". RSGrapher can be initiated on the command line with:

    python run.pyw
###Requirements
Requires Python 3.5 or later to run. Install necessary modules with the command:

    python -m pip install -r requirements.txt

## Abstract
RSGrapher is an application meant to streamline the analysis and reporting of rebar stress data.
A **test** consists of pulling multiple samples of rebar with a massive machine to the point of
failure. During testing, the **time**, **strain** (displacement) and **stress** (load) are recorded in ~.2 second intervals.
The resulting data is returned as a text file, which RSGrapher parses into its internal data structure.

The main purpose of RSGrapher is to scale and shift this data to produce three graphs that describe several significant characteristics of the sample:
* **Peak Load**: The maximum load handled by the sample. Also called _Ultimate Tensile Strength_
when working with stress (load per unit cross-sectional area).
* **Yield Load**: The "yield point" of the sample; the point where the material loses elasticity and begins deforming plastically.