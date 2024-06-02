# Scalable Molecular Simulation of Electrolyte Solutions with Quantum Chemical Accuracy

This repository contains the data and scripts necessary to reproduce the results presented in the paper:
**"Scalable molecular simulation of electrolyte solutions with quantum chemical accuracy"** by Junji Zhang, Joshua Pagotto, Tim Gould, and Timothy T. Duignan.

## Contents

- **Figs.ipynb**: A Jupyter notebook that calculates all key quantities and generates all plots using the raw data found in the `Data` directory.
- **Input Files**:
  - **CP2K**: Contains input files used to generate the training data with CP2K.
  - **NequIP**: Contains Nequip training config files and trained models.
  - **LAMMPS**: Contains LAMMPS files to run the NNP-MD simulations.
  - **Scripts**: Includes various scripts for converting file formats and computing Radial Distribution Functions (RDFs).

## Contact

For access to the raw trajectories or if you plan to use this code to run simulations of a new electrolyte (to avoid redundant calculations), please contact Tim Duignan at [tim@duignan.net](mailto:tim@duignan.net).

---

Feel free to reach out with any questions or for further assistance.

---

### Acknowledgements

We appreciate the contributions of all authors and collaborators in this research project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======

