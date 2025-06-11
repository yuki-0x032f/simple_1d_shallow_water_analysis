# Simple 1D Shallow Water Analysis

This project is a Python package for analyzing one-dimensional shallow water flow. It can perform simple calculations with constant bed slope, channel width, and boundary conditions.

## Requirements

- Python 3.13 or higher
- Dependencies:
  - numpy (>=2.3.0)
  - matplotlib (>=3.10.3)
  - pyyaml (>=6.0.2)

## Installation

You can install using Poetry:

```bash
poetry install
```

## Project Structure

```
.
├── README.md
├── pyproject.toml
├── poetry.lock
├── swe/
│   ├── __init__.py
│   ├── solver.py      # Main computational logic for numerical analysis
│   └── utils.py       # Utility functions
├── examples/
    ├── main.py        # Usage example
    ├── result/        # Calculation result
    └── conditions.yml # Configuration file for calculation conditions
```

## Usage

1. Configure calculation conditions in `examples/conditions.yml`:
   - Channel length
   - Calculation time
   - Spatial and temporal discretization
   - Bed slope
   - Discharge (unit width discharge)
   - Manning's roughness coefficient

2. Run the calculation:

```bash
python -m examples.main 
```

3. Results are saved in the `result/` directory.

4. Optionally, images can be converted to video using ffmpeg.
```bash
ffmpeg -i result/%04d.png -pix_fmt yuv420p animation.mp4
```

## License

This project is released under the MIT License.

## References

- [Numeriacl Hydraulics](https://i-ric.org/yasu/nbook2/index.html) - Comprehensive guide on shallow water flow numerical methods

## Author

- yuki (you.ki.0815@icloud.com)