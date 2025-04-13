import numpy as np
import pandas as pd
import streamlit as st
import rateslib as rl
from rateslib.curves import Curve
from rateslib.instruments import IRS

# Example: Create a basic curve
curve = Curve(
    nodes=[0.25, 0.5, 1.0, 2.0, 5.0, 10.0],
    values=[0.01, 0.012, 0.015, 0.018, 0.022, 0.025]
)

# Price an Interest Rate Swap
swap = IRS(effective="2025-01-01", termination="2030-01-01", fixed_rate=0.02, curves={"disc": curve, "fwd": curve})
npv = swap.npv()
print(f"Swap NPV: {npv:.2f}")

