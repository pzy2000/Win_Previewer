import os
import pytest
from main import load_blacklist, save_blacklist, blacklist


def test_load_blacklist(tmpdir):
    # Create a temporary blacklist.txt file
    temp_file = tmpdir.join("blacklist.txt")
    temp_file.write("Notepad\nCalculator\n")

    # Change the working directory to the temporary directory
    os.chdir(tmpdir)

    load_blacklist()

    # Check if the blacklist contains the correct items
    assert len(blacklist) == 0


def test_save_blacklist(tmpdir):
    # Setup the blacklist
    blacklist.clear()
    blacklist.add("Notepad")
    blacklist.add("Calculator")

    # Save the blacklist to a temporary file
    temp_file = tmpdir.join("blacklist.txt")
    save_blacklist()

    # Verify the file content
    with open(temp_file, "r") as f:
        lines = f.readlines()

    assert "Notepad\n" in lines
    assert "Calculator\n" in lines
    assert len(lines) == 2


def test_add_to_blacklist():
    # Clear the blacklist and add an item
    blacklist.clear()
    blacklist.add("NewApp")

    # Save and reload the blacklist
    save_blacklist()
    load_blacklist()

    # Check that the item is in the blacklist
    assert "NewApp" in blacklist


def test_remove_from_blacklist():
    # Setup the blacklist with some items
    blacklist.clear()
    blacklist.add("AppToRemove")

    # Remove the item
    blacklist.remove("AppToRemove")

    # Save and reload the blacklist
    save_blacklist()
    load_blacklist()

    # Check that the item is not in the blacklist
    assert "AppToRemove" not in blacklist

