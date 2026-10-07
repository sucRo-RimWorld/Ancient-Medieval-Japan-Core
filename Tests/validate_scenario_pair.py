"""Project actual Grains + separate Scenarios explicit XML (not engine/save tests)."""
import argparse
from pathlib import Path
import test_scenario_extraction as contracts

def validate(scenario):
    contracts.GRAINS_ID = 'sucro.ancientmedievaljapan.core'
    contracts.SCENARIO_ID = 'sucro.ancientmedievaljapan.scenarios'
    for mo in (False,True):
        for grains,addon in ((True,False),(False,True),(True,True)):
            packages=([contracts.ROOT] if grains else [])+([scenario] if addon else [])
            contracts.check(packages,grains,addon,mo)
    print('Actual repository pair: six explicit XML provider/contract configurations PASS; runtime/save unverified.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario-root',type=Path,required=True)
    validate(parser.parse_args().scenario_root.resolve())
