# Stacks

[Sublime Text](https://www.sublimetext.com/) plugin to manage collections of views under different circumstances.

A **stack** is a collection of views and its current layout.

## When would you need this?

When you are working on a feature or a bug in a large codebase (some say they are the same thing!), you can quickly open a lot of files related to the problem you are working on.

When you temporarily switch to a new problem you have to close all the related files you were working on in the previous problem. If you need to resume your work on your previous problem, you need to figure out all the relate files to continue your work. That's annoying and has high friction.

With *Stacks* you can just save all the related views in one go with a handy name and reload to it later. Stacks allows you to save your context in terms of views and layouts.


![](stacks.gif)


## Installation

- Open the command palette with `CMD + SHIFT + P`
- Select `Package Control: Add Repository`
- Enter https://github.com/ssanj/Stacks for the repository
- Select `Package Control: Install Package`
- Choose Stacks


## Functionality

### Save a stack

Save the current view stack with  `F2`

### Load a stack

Load a given stack with  `SHIFT + F2`

### Delete a stack

Delete a given stack with `CTRL + SHIFT + F2`

### Rename a stack

Rename a stack with `SHIFT + CMD + F2`

### Close active stack

Close an active stack with `CTRL + SHIFT + CMD + F2`

### View the current stack name

View the current stack name via the command palette with `Stacks: Show Stack Name`
