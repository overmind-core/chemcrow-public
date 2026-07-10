from rdkit import RDLogger

# Silence RDKit's noisy C++ logger (deprecation notices and expected SMILES
# parse errors from input-type sniffing) so agent traces stay readable.
RDLogger.DisableLog("rdApp.*")

from .tools.rdkit import *
from .tools.search import *
from .frontend import *
from .agents import ChemCrow, make_tools
from .version import __version__
