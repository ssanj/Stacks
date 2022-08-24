# persisted format

```json
  [
    {
      "my stack 1": {
        "group0": [
              "/Volumes/Work/projects/code/python/sublime_plugins/Stacks/stacks.py",
              "/Volumes/Work/projects/code/python/sublime_plugins/Stacks/.python-version",
              "/Volumes/Work/projects/code/python/sublime_plugins/Stacks/Default.sublime-commands",
              "/Volumes/Work/projects/code/python/sublime_plugins/Stacks/run-tests"
        ],
        "group1": [],
        "layout": {"cells": [[0, 0, 1, 1], [0, 1, 1, 2]], "cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0]}
      }
    }
  ]
```

# MVPs

1. Save the current view names to a json file and close all views in the window [x]
1. Read the saved view names from the json file and load them into the window [x]
1. Prompt the user for a stack name before saving the stack [x]
1. Save the stack to the user-supplied stack key within the persisted config [x]
1. Expand config to above format (without groups and layout) [x]
1. Drop list of saved stacks when the user wants to load a stack [x]
1. Load stack and open views [x]
1. Allow the user to delete a stack by name [x]
1. Allow saving back to the existing stack (if you already opened it) [x]
1. Show stack name on status bar
1. Add logging through Logger
1. Prompt before closing all tabs [x]
1. Move out common functions that return an ADT (open_stack, save_stack)
1. Rename stack?

# Questions

1. Do we want to close all open views on saving and loading stacks?
1. Do we want to persist the whole window or just the second group?
1. Do we need to allow renaming of stacks? (delete + save)
1. Do we need a view to preview existing stacks?
