import pytest
from shutil import copytree

from pkgpanda.util import is_windows, resources_test_dir, run


list_output = """mesos:
  0.22.0
  0.23.0
mesos-config:
  ffddcfb53168d42f92e4771c6f8a8a9a818fd6b8
  justmesos
"""

active_output = """mesos--0.22.0
mesos-config--ffddcfb53168d42f92e4771c6f8a8a9a818fd6b8
"""

list_remove_output = """mesos--0.23.0
mesos-config:
  ffddcfb53168d42f92e4771c6f8a8a9a818fd6b8
  justmesos
"""

@pytest.mark.skipif(not is_windows)
def test_list_windows():
    repo = "--repository={}".format(resources_test_dir("packages"))
    test_output = run(["pkgpanda", "list", repo])
    test_output = test_output.replace('\r', '')   # Eliminate the CRs that windows inserts
    print("test_output: "+test_output)
    print("list_output: "+list_output)
    assert test_output == list_output


@pytest.mark.skipif(not is_windows)
def test_active_windows():
    test_output = run(["pkgpanda", "active", "--root={}".format(resources_test_dir("install"))])
    test_output = test_output.replace('\r', '')   # Eliminate the CRs that windows inserts
    print("test_output: "+test_output)
    print("list_output: "+list_output)
    assert test_output == active_output


@pytest.mark.skipif(not is_windows)
def test_remove_windows(tmpdir):
    repo_dir = str(tmpdir.join("repo"))
    copytree(resources_test_dir("packages"), repo_dir)
    assert run([
        "pkgpanda",
        "remove",
        "mesos--0.22.0",
        "--repository={}".format(repo_dir),
        "--root={}".format(resources_test_dir("install_empty"))])

    test_output = run(["pkgpanda", "list", "--repository={}".format(repo_dir)])
    test_output = test_output.replace('\r', '')   # Eliminate the CRs that windows inserts
    print("test_output: "+test_output)
    print("list_remove_output: "+list_remove_output)
    assert test_output == list_remove_output
    # TODO(cmaloney): Test removing a non-existant package.
    # TODO(cmaloney): Test removing an active package.
