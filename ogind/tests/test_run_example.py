"""
This model tests whether using the `OG-IND/examples/run_og_ind.py`
work by making sure that it does not break (is still running) after
5 minutes (300 seconds).
"""
import multiprocessing
import time
import os
import sys
import importlib.util
from pathlib import Path
import pytest


def call_run_og_ind():
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    path = Path(cur_path)
    roe_fldr = os.path.join(path.parent.parent, "examples")
    roe_file_path = os.path.join(roe_fldr, "run_og_ind.py")
    spec = importlib.util.spec_from_file_location(
        "run_og_ind.py", roe_file_path
    )
    roe_module = importlib.util.module_from_spec(spec)
    sys.modules["run_og_ind.py"] = roe_module
    spec.loader.exec_module(roe_module)
    roe_module.main()


@pytest.mark.local
def test_run_og_ind(f=call_run_og_ind):
    p = multiprocessing.Process(target=f, name="run_og_ind", args=())
    p.start()
    time.sleep(300)
    if p.is_alive():
        p.terminate()
        p.join()
        timetest = True
    else:
        print("run_og_ind.py did not run for minimum time")
        timetest = False
    print("timetest ==", timetest)

    assert timetest
