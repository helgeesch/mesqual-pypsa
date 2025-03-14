[![Python >=3.10](https://img.shields.io/badge/python-≥3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

# MESCAL PyPSA <img src="https://raw.githubusercontent.com/helgeesch/mescal/0fd73109a9dd36611c3669987229e2b50ba6ec98/assets/logo_no_text_no_bg.svg" width="70" height="70" alt="logo">
This is the [mescal](https://github.com/helgeesch/mescal)-interface package for [PyPSA](https://github.com/PyPSA/PyPSA) Network objects.

## Minimum usage examples

#### Example to set up a study with multiple scenarios and scenario comparisons from pypsa Networks

```python
import pypsa
from mescal import StudyManager
from mescal_pypsa import PyPSADataset

# Load networks
n_base = pypsa.Network('your_base_network.nc')
n_scen1 = pypsa.Network('your_scen1_network.nc')
n_scen2 = pypsa.Network('your_scen2_network.nc')

# Initialize study manager
study = StudyManager.factory_from_scenarios(
    scenarios=[
        PyPSADataset(n_base, name='base'),
        PyPSADataset(n_scen1, name='scen1'),
        PyPSADataset(n_scen2, name='scen2'),
    ],
    comparisons=[("scen1", "base"), ("scen2", "base")],
    export_folder="output"
)

# Access MultiIndex df with data for all scenarios
df_prices = study.scen.fetch("buses_t.marginal_price")

# Access MultiIndex df with data for all comparisons (delta values)
df_price_deltas = study.comp.fetch("buses_t.marginal_price")

# Access buses model df of base case
df_bus_model = study.scen.get_dataset('base').fetch('buses')
```

For more hands-on examples and see mescal-pypsa in action, please visit the [mescal-vanilla-studies](https://github.com/helgeesch/mescal-vanilla-studies) repo and check out the example studies.

---

## Getting Started: Integrate mescal and mescal-pypsa packages in your project
In order to make use of mescal-pypsa, you will need to integrate it together with the foundation package [mescal](https://github.com/helgeesch/mescal) as submodules in your project. 
Please follow the instructions found in [mescal](https://github.com/helgeesch/mescal)'s README.md, or check out the [mescal-vanilla-studies](https://github.com/helgeesch/mescal-vanilla-studies) repo and replicate the repo architecture + Getting Started steps for your project. 

---

## Attribution and Licenses
This project is licensed under the LGPL License - see the LICENSE file for details.

MESCAL-pypsa is to be used in combination with the popular [PyPSA](https://github.com/PyPSA/PyPSA) toolbox [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14960992.svg)](https://doi.org/10.5281/zenodo.14960992) - [MIT license]

---

## Contact

For questions or feedback about MESCAL or these example studies, don't hesitate to get in touch!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/helge-e-8201041a7/)