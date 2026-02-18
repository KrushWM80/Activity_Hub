# Ignore Build in Source Contrl

* Status: accepted
* Deciders: [Cory Reed, Isaac Baron]
* Date: 2024-03-06

Technical Story: [description | ticket/issue URL] <!-- optional -->

## Context and Problem Statement

Tracking build artifacts as decided in [Store Built Tokens in Source Control](0002-built-tokens-in-source-control.md) has led to problems with developer experience when contributing and reviewing pull requests.

## Decision Drivers

* Developer experience

## Considered Options

### 0. Do nothing

Keep tracking built tokens in source control

* Good, because no change
* Bad, because a time-consuming script is run on git's pre-commit hook
* Bad, because it's difficult to review pull requests due to the amount of built token changes

### 1. Remove built tokens from source control 

* Good, because no need for running the time-consuming script on git's pre-commit hook
* Good, because it will be easier to review pull requests
* Bad, because it requires some work
* Bad, because tracking changes in built tokens is more difficult

## Decision Outcome

Chosen option: 1. Remove build tokens from source control. because it will improve the developer experience.