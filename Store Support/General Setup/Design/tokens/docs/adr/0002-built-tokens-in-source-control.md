# Store Built Tokens in Source Control

* Status: Superceded by [Ignore Build in Source Control](0003-ignore-build-in-source-control.md)
* Deciders: [Cory Reed, Derrique Balayut, Douglas Kazumi, Isaac Baron, Jordan Lu, Kenam Verma, Sheetal Yadav, Shubham Sapra, Zachary Heusinkveld]
* Date: 2022-01-10

## Context and Problem Statement

Currently, there is no automated mechanism to identify updates to built tokens after a change has been committed to the Living Design tokens repository. This makes it more difficult than necessary to identify what has been changed in the published token packages for each platform, leading to the possibility of unintended changes and regressions.

As of now, updates to the tokens build pipeline require an ad hoc diff to identify how built tokens have been affected. There is no built-in process to review those changes, leaving the task of identifying which outputted tokens have changed to developers/reviewers. The tokens build pipeline contains shared functionality between platforms, further increasing the likelihood of unintentional cross-platform changes.

There is precedent in open source for design systems storing dist/ tokens in source control. (See Links section below).

## Decision Drivers

* Developer experience (speed of delivery and ease of use)
* Likelihood of unintended changes to distributed tokens
* Solution LOE

## Considered Options

### 0. Do nothing

* Good, because there is no effort involved
* Bad, because there is a higher likelihood of introducing unintended changes and regressions

### 1. Store built tokens in source control

Store tokens build output in source-control and add a pre-commit build step to ensure the latest version of token variables are included in commits. Any changes to built tokens will be reviewed alongside changes to token definitions and configuration changes.

* Good, because any changes to token variables are immediately visible, significantly lowering the chance of unintended changes
* Good, because after the initial implementation, the change to development process is minimal
* Bad, because pre-commit hooks require maintenance and may cause annoyances for developers

## Decision Outcome

Chosen option: 1. Store built tokens in source control.

## Links

Open source design system design tokens with output in source:

* <https://github.com/kiwicom/orbit/tree/master/packages/orbit-design-tokens/output>
* <https://github.com/FirefoxUX/design-tokens>
* <https://github.com/Shopify/polaris-tokens/tree/main/dist>
* <https://github.com/rei/rei-cedar-tokens/tree/next/dist>
