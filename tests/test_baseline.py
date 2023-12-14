import jellyfin
import pytest


def test_version():
    expected_version = jellyfin.__version__
    filepath = "./src/jellyfin/__init__.py"
    with open(filepath, "r") as file:
        line = file.readline()
        version = line.split("=")[1].strip().strip('"')
        assert (
            version == expected_version
        ), f"Expected version is {expected_version}, but got {version}"


if __name__ == "__main__":
    pytest.main()
