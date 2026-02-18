# CHANGELOG

[comment]: # 'REPO ONLY START'

Contents:

- [CHANGELOG](#changelog)
  - [Release 2.2.7](#release-227)
  - [Release 2.2.7-rc.2](#release-227-rc2)
  - [Release 2.2.7-rc.1](#release-227-rc1)
  - [Release 2.2.7-rc.0](#release-227-rc0)
  - [Release 2.2.6](#release-226)
  - [Release 2.2.6-rc.2](#release-226-rc2)
  - [Release 2.2.6-rc.1](#release-226-rc1)
  - [Release 2.2.6-rc.0](#release-226-rc0)
  - [Release 2.2.5](#release-225)
    - [Internal](#internal)
  - [Release 2.2.5-rc.2](#release-225-rc2)
  - [Release 2.2.5-rc.1](#release-225-rc1)
    - [Internal](#internal-1)
  - [Release 2.2.5-rc.0](#release-225-rc0)
    - [Internal](#internal-2)
  - [Release 2.2.4](#release-224)
  - [Release 2.2.4-rc.4](#release-224-rc4)
  - [Release 2.2.4-rc.3](#release-224-rc3)
  - [Release 2.2.4-rc.2](#release-224-rc2)
  - [Release 2.2.4-rc.1](#release-224-rc1)
  - [Release 2.2.4-rc.0](#release-224-rc0)
  - [Release 2.2.3](#release-223)
  - [Release 2.2.3-rc.1](#release-223-rc1)
  - [Release 2.2.3-rc.0](#release-223-rc0)
  - [Release 2.2.2](#release-222)
    - [Internal](#internal-3)
  - [Release 2.2.2-rc.1](#release-222-rc1)
  - [Release 2.2.2-rc.0](#release-222-rc0)
    - [Internal](#internal-4)
  - [Release 2.2.1](#release-221)
    - [Breaking changes](#breaking-changes)
  - [Release 2.2.1-rc.1](#release-221-rc1)
  - [Release 2.2.1-rc.0](#release-221-rc0)
    - [Breaking changes](#breaking-changes-1)
  - [Release 2.2.0](#release-220)
  - [Release 2.1.10](#release-2110)
  - [Release 2.1.9](#release-219)
  - [Release 2.1.8](#release-218)
    - [Deprecated](#deprecated)
  - [Release 2.1.7](#release-217)
  - [Release 2.1.6](#release-216)
  - [Release 2.1.5](#release-215)
  - [Release 2.1.4](#release-214)
  - [Release 2.1.3](#release-213)
  - [Release 2.1.2](#release-212)
  - [Release 2.1.1](#release-211)
  - [Release 2.1.0](#release-210)
  - [Breaking changes](#breaking-changes-2)
  - [Release 2.0.10](#release-2010)
    - [Breaking changes](#breaking-changes-3)
  - [Release 2.0.9](#release-209)
  - [Release 2.0.8](#release-208)
  - [Release 2.0.7](#release-207)
  - [Release 2.0.6](#release-206)
  - [Release 2.0.5](#release-205)
  - [Release 2.0.4](#release-204)
  - [Release 2.0.3](#release-203)
  - [Release 2.0.2](#release-202)
  - [Release 2.0.1](#release-201)
  - [Release 2.0.0](#release-200)
    - [Overview](#overview)
    - [Breaking changes](#breaking-changes-4)
    - [Changed](#changed)
      - [Alignment with LD3 specs](#alignment-with-ld3-specs)
      - [Imports](#imports)
      - [Other examples of before / after the upgrade](#other-examples-of-before--after-the-upgrade)
    - [Migration using Codemods](#migration-using-codemods)
      - [Usage](#usage)
      - [Included Transforms](#included-transforms)
        - [updateImports](#updateimports)
        - [updateJestConfig](#updatejestconfig)
        - [updateStyle](#updatestyle)
      - [Example app](#example-app)
      - [Picker dependencies](#picker-dependencies)
    - [Added](#added)
      - [Fonts](#fonts)
      - [Icons](#icons)
  - [Release 2.0.0 tickets:](#release-200-tickets)
  - [Release 2.0.0-rc.2](#release-200-rc2)
  - [Release 2.0.0-rc.1](#release-200-rc1)
  - [Release 2.0.0-beta.11](#release-200-beta11)
  - [Release 2.0.0-beta.10](#release-200-beta10)
  - [Release 2.0.0-beta.9](#release-200-beta9)
  - [Release 2.0.0-beta.8](#release-200-beta8)
  - [Release 2.0.0-beta.7](#release-200-beta7)
  - [Release 2.0.0-beta.6](#release-200-beta6)
  - [Release 2.0.0-beta.5](#release-200-beta5)
  - [Release 2.0.0-beta.4](#release-200-beta4)
  - [Release 2.0.0-beta.3](#release-200-beta3)
  - [Release 2.0.0-beta.2](#release-200-beta2)
  - [Releases prior to 2.0](#releases-prior-to-20)
  - [Release 1.8.18](#release-1818)
    - [Fixed](#fixed)
  - [Release 1.8.17](#release-1817)
    - [Fixed](#fixed-1)
  - [Release 1.8.16](#release-1816)
    - [Fixed](#fixed-2)
  - [Release 1.8.15](#release-1815)
    - [Fixed](#fixed-3)
  - [Release 1.8.14](#release-1814)
    - [Fixed](#fixed-4)
  - [Release 1.8.13](#release-1813)
    - [Fixed](#fixed-5)
  - [Release 1.8.12](#release-1812)
    - [Fixed](#fixed-6)
  - [Release 1.8.11](#release-1811)
    - [Fixed](#fixed-7)
  - [Release 1.8.10](#release-1810)
    - [Fixed](#fixed-8)
    - [Added](#added-1)
  - [Release 1.8.9](#release-189)
    - [Fixed](#fixed-9)
    - [Added](#added-2)
  - [Release 1.8.8](#release-188)
    - [Fixed](#fixed-10)
  - [Release 1.8.7](#release-187)
    - [Added](#added-3)
  - [Release 1.8.6](#release-186)
    - [Fixed](#fixed-11)
  - [Release 1.8.5](#release-185)
    - [Added](#added-4)
  - [Release 1.8.4](#release-184)
    - [Added](#added-5)
  - [Release 1.8.3](#release-183)
    - [Fixed](#fixed-12)
  - [Release 1.8.2](#release-182)
    - [Added](#added-6)
  - [Release 1.8.1](#release-181)
    - [Added](#added-7)
  - [Release 1.8.0](#release-180)
    - [Added](#added-8)
    - [Changed](#changed-1)
    - [Fixed](#fixed-13)
  - [Release 1.7.3](#release-173)
    - [Added](#added-9)
  - [Release 1.7.2](#release-172)
    - [Added](#added-10)
    - [Fixed](#fixed-14)
  - [Release 1.7.1](#release-171)
    - [Fixed](#fixed-15)
  - [Release 1.7.0](#release-170)
    - [Breaking](#breaking)
    - [Added](#added-11)
    - [Changed](#changed-2)
    - [Fixed](#fixed-16)
  - [Release 1.6.0](#release-160)
    - [Added](#added-12)
    - [Changed](#changed-3)
    - [Fixed](#fixed-17)
  - [Release 1.5.1](#release-151)
    - [Changed](#changed-4)

[comment]: # 'REPO ONLY END'

## Release 2.2.7

- [CEEMP-3797](https://jira.walmart.com/browse/CEEMP-3797) - modal off-white background color bug [#791](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/791)
- [CEEMP-3745](https://jira.walmart.com/browse/CEEMP-3745) BottomSheet custom title accessibilityLabel fix [#783](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/783)
- [CEEMP-3789](https://jira.walmart.com/browse/CEEMP-3789) BottomSheet flickering fix [#787](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/787)
- [CEEMP-3802](https://jira.walmart.com/browse/CEEMP-3802) BottomSheet overlapping when keyboard open RN>76 fix [#789](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/789)
- [CEEMP-3747](https://jira.walmart.com/browse/CEEMP-3747) Fix Bottomsheet multiple onOpen calls [#723](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/723)

## Release 2.2.7-rc.2

- [CEEMP-3797](https://jira.walmart.com/browse/CEEMP-3797) - modal off-white background color bug [#791](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/791)

## Release 2.2.7-rc.1

- [CEEMP-3745](https://jira.walmart.com/browse/CEEMP-3745) BottomSheet custom title accessibilityLabel fix [#783](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/783)
- [CEEMP-3789](https://jira.walmart.com/browse/CEEMP-3789) BottomSheet flickering fix [#787](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/787)
- [CEEMP-3802](https://jira.walmart.com/browse/CEEMP-3802) BottomSheet overlapping when keyboard open RN>76 fix [#789](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/789)

## Release 2.2.7-rc.0

- [CEEMP-3747](https://jira.walmart.com/browse/CEEMP-3747) Fix Bottomsheet multiple onOpen calls [#723](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/723)

## Release 2.2.6

- [CEEMP-3742](https://jira.walmart.com/browse/CEEMP-3742) Fix TextField label accessibility [#714](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/714)
- [CEEMP-3682](https://jira.walmart.com/browse/CEEMP-3682) Select error text auto focus when talk back on [#710](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/710)
- [CEEMP-3743](https://jira.walmart.com/browse/CEEMP-3743) Fix BotttomSheet freeze [#709](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/709)
- [CEEMP-3741](https://jira.walmart.com/browse/CEEMP-3741) Select Voice over issue fix and example added with sample [#700](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/700)
- [CEEMP-3734](https://jira.walmart.com/browse/CEEMP-3734) BottomSheet onClose/onClosed callback fixes [#685](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/685)
- [CEEMP-3732](https://jira.walmart.com/browse/CEEMP-3732) Filter Toggle accessibility fixes [#684](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/684)
- [CEEMP-3733](https://jira.walmart.com/browse/CEEMP-3733) Fix BottomSheet close animation [#683](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/683)
- [CEEMP-3680](https://jira.walmart.com/browse/CEEMP-3680) BottomSheet onClose fix [#657](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/657)
- [CEEMP-3681](https://jira.walmart.com/browse/CEEMP-3681) Feature Request - Styling Select label w/ accessibility [#652](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/652)
- [CEEMP-3712](https://jira.walmart.com/browse/CEEMP-3712) Metric optional chevron right prop [#659](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/659)

## Release 2.2.6-rc.2

- [CEEMP-3682](https://jira.walmart.com/browse/CEEMP-3682) Select error text auto focus when talk back on [#710](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/710)
- [CEEMP-3743](https://jira.walmart.com/browse/CEEMP-3743) Fix BotttomSheet freeze [#709](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/709)
- [CEEMP-3741](https://jira.walmart.com/browse/CEEMP-3741) Select Voice over issue fix and example added with sample [#700](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/700)

## Release 2.2.6-rc.1

- [CEEMP-3734](https://jira.walmart.com/browse/CEEMP-3734) BottomSheet onClose/onClosed callback fixes [#685](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/685)
- [CEEMP-3732](https://jira.walmart.com/browse/CEEMP-3732) Filter Toggle accessibility fixes [#684](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/684)
- [CEEMP-3733](https://jira.walmart.com/browse/CEEMP-3733) Fix BottomSheet close animation [#683](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/683)

## Release 2.2.6-rc.0

- [CEEMP-3680](https://jira.walmart.com/browse/CEEMP-3680) BottomSheet onClose fix [#657](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/657)
- [CEEMP-3681](https://jira.walmart.com/browse/CEEMP-3681) Feature Request - Styling Select label w/ accessibility [#652](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/652)
- [CEEMP-3712](https://jira.walmart.com/browse/CEEMP-3712) Metric optional chevron right prop [#659](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/659)

## Release 2.2.5

- [CEEMP-3597](https://jira.walmart.com/browse/CEEMP-3597) Decoupled RNModal [#650](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/650)
- [CEEMP-3662](https://jira.walmart.com/browse/CEEMP-3662) Alert Accessibility focus issue and icon label issue fix [#647](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/647)
- [CEEMP-3597](https://jira.walmart.com/browse/CEEMP-3597) Decoupled BottomSheet component [#644](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/644)
- [CEEMP-3666](https://jira.walmart.com/browse/CEEMP-3666) TabNavigationItem width fix when orientation change [#645](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/645)
- [CEEMP-3656](https://jira.walmart.com/browse/CEEMP-3656) TabNavigationItem accessibility fix [#637](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/637)
- [CEEMP-3651](https://jira.walmart.com/browse/CEEMP-3651) ProgressTrackerItem accessibilityLabel fixes [#635](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/635)
- [CEEMP-3610](https://jira.walmart.com/browse/CEEMP-3610) Added string check for children of the DataTableCell [#627](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/627)
- [CEEMP-3505](https://jira.walmart.com/browse/CEEMP-3505) Metric/MetricGroup Accessibility issue fix [#624](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/624)
- [CEEMP-3486](https://jira.walmart.com/browse/CEEMP-3486) Metric/MetricGroup onPress functionality added [#623](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/623)
- [CEEMP-3530](https://jira.walmart.com/browse/CEEMP-3530) expose disabled prop on DateDropdown [#626](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/626)
- [CEEMP-3487](https://jira.walmart.com/browse/CEEMP-3487) Metric with card [#615](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/615)

### Internal

- [CEEMP-3605](https://jira.walmart.com/browse/CEEMP-3605) Add Dark mode support to Example App [#625](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/625)
- [CEEMP-3622](https://jira.walmart.com/browse/CEEMP-3622) config looper to run yarn 4.4.1 [#631](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/631)
- [CEEMP-3494](https://jira.walmart.com/browse/CEEMP-3494) Typography added and Docusaurus upgraded to 3.4.0 [#606](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/606)
- (chore) add code owners [#608](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/608)

## Release 2.2.5-rc.2

- [CEEMP-3597](https://jira.walmart.com/browse/CEEMP-3597) Decoupled RNModal [#650](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/650)

## Release 2.2.5-rc.1

- [CEEMP-3662](https://jira.walmart.com/browse/CEEMP-3662) Alert Accessibility focus issue and icon label issue fix [#647](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/647)
- [CEEMP-3597](https://jira.walmart.com/browse/CEEMP-3597) Decoupled BottomSheet component [#644](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/644)
- [CEEMP-3666](https://jira.walmart.com/browse/CEEMP-3666) TabNavigationItem width fix when orientation change [#645](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/645)
- [CEEMP-3656](https://jira.walmart.com/browse/CEEMP-3656) TabNavigationItem accessibility fix [#637](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/637)
- [CEEMP-3651](https://jira.walmart.com/browse/CEEMP-3651) ProgressTrackerItem accessibilityLabel fixes [#635](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/635)
- [CEEMP-3610](https://jira.walmart.com/browse/CEEMP-3610) Added string check for children of the DataTableCell [#627](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/627)
- [CEEMP-3505](https://jira.walmart.com/browse/CEEMP-3505) Metric/MetricGroup Accessibility issue fix [#624](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/624)
- [CEEMP-3486](https://jira.walmart.com/browse/CEEMP-3486) Metric/MetricGroup onPress functionality added [#623](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/623)
- [CEEMP-3530](https://jira.walmart.com/browse/CEEMP-3530) expose disabled prop on DateDropdown [#626](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/626)
- [CEEMP-3487](https://jira.walmart.com/browse/CEEMP-3487) Metric with card [#615](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/615)

### Internal

- [CEEMP-3605](https://jira.walmart.com/browse/CEEMP-3605) Add Dark mode support to Example App [#625](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/625)
- [CEEMP-3622](https://jira.walmart.com/browse/CEEMP-3622) config looper to run yarn 4.4.1 [#631](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/631)

## Release 2.2.5-rc.0

### Internal

- [CEEMP-3494](https://jira.walmart.com/browse/CEEMP-3494) Typography added and Docusaurus upgraded to 3.4.0 [#606](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/606)
- (chore) add code owners [#608](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/608)

## Release 2.2.4

- [CEEMP-3517](https://jira.walmart.com/browse/CEEMP-3517) TextField and TextArea accessibility fix [#618](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/618)
- [CEEMP-3516](https://jira.walmart.com/browse/CEEMP-3516) fix select border padding [#617](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/617)
- [CEEMP-3519](https://jira.walmart.com/browse/CEEMP-3519) Fix Checkbox accessibility label [#616](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/616)
- [CEEMP-3508](https://jira.walmart.com/browse/CEEMP-3508) add spotlightColor and adjust offset. Adding spotlight feature to Popover [#613](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/613) [#610](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/610)
- [CEEMP-3504](https://jira.walmart.com/browse/CEEMP-3504) Fixes for Select going out of array range [#607](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/607)
- [CEEMP-3468](https://jira.walmart.com/browse/CEEMP-3468) fixes for BottomSheet onClose called automatically [#602](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/602)

## Release 2.2.4-rc.4

- [CEEMP-3517](https://jira.walmart.com/browse/CEEMP-3517) TextField and TextArea accessibility fix [#618](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/618)
- [CEEMP-3516](https://jira.walmart.com/browse/CEEMP-3516) Fix select border padding [#617](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/617)
- [CEEMP-3519](https://jira.walmart.com/browse/CEEMP-3519) Fix Checkbox accessibility label [#616](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/616)

## Release 2.2.4-rc.3

- [CEEMP-3508](https://jira.walmart.com/browse/CEEMP-3508) add spotlightColor and adjust offset [#613](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/613)

## Release 2.2.4-rc.2

- [CEEMP-3508](https://jira.walmart.com/browse/CEEMP-3508) Adding spotlight feature to Popover [#610](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/610)

## Release 2.2.4-rc.1

- [CEEMP-3504](https://jira.walmart.com/browse/CEEMP-3504) Fixes Select going out of array range [#607](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/607)

## Release 2.2.4-rc.0

- [CEEMP-3468](https://jira.walmart.com/browse/CEEMP-3468) fixes for BottomSheet onClose called automatically [#602](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/602)

## Release 2.2.3

- [CEEMP-3433](https://jira.walmart.com/browse/CEEMP-3433) Upgraded React Native to 0.73.8 [#589](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/589)
- (fix) update gtp-shared-icons to 1.0.10 [#600](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/600)

## Release 2.2.3-rc.1

- (fix) update gtp-shared-icons to 1.0.10 [#600](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/600)

## Release 2.2.3-rc.0

- [CEEMP-3433](https://jira.walmart.com/browse/CEEMP-3433) Upgraded React Native to 0.73.8 [#589](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/589)

## Release 2.2.2

- [CEEMP-3426](https://jira.walmart.com/browse/CEEMP-3426) Refresh icons to include SlidersIcon [#593](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/593)
- [CEEMP-3425](https://jira.walmart.com/browse/CEEMP-3425) progressIndicator fixwidth fix [#582](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/582)
- [CEEMP-3401](https://jira.walmart.com/browse/CEEMP-3401) RNModal props are exposed for Modal/BottomSheet/Select [#587](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/587)
- [CEEMP-3395](https://jira.walmart.com/browse/CEEMP-3395) ProgressIndicator render fix [#581](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/581)
- [CEEMP-3439](https://jira.walmart.com/browse/CEEMP-3439) BottomSheet Actions Space issue fix [#586](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/586)
- [CEEMP-3234](https://jira.walmart.com/browse/CEEMP-3234) Feature Request - Add containerStyle to Chips
- [CEEMP-3280](https://jira.walmart.com/browse/CEEMP-3280) Migrate documentation from Styleguidist to Docusaurus
- [CEEMP-3276](https://jira.walmart.com/browse/CEEMP-3276) Select accessibility more props fixes
- [CEEMP-3363](https://jira.walmart.com/browse/CEEMP-3363) Bottomsheet content scroll issue fix
- [CEEMP-3380](https://jira.walmart.com/browse/CEEMP-3380) Feature Request - Add Color prop to Typography components
- [CEEMP-3359](https://jira.walmart.com/browse/CEEMP-3359) Bug Report - nativeID for TextField label
- [CEEMP-3342](https://jira.walmart.com/browse/CEEMP-3342) Feature Request - use native Spinner
- [CEEMP-3254](https://jira.walmart.com/browse/CEEMP-3254) Update LD tokens to latest v0.74

### Internal

- [CEEMP-3314](https://jira.walmart.com/browse/CEEMP-3314) Refactor DateDropdown to align with new example app structure
- [CEEMP-3312](https://jira.walmart.com/browse/CEEMP-3312) Refactor Switch to align with new example app structure
- [CEEMP-3309](https://jira.walmart.com/browse/CEEMP-3309) Refactor Checkbox to align with new example app structure
- [CEEMP-3308](https://jira.walmart.com/browse/CEEMP-3308) Refactor Radio to align with new example app structure
- [CEEMP-3316](https://jira.walmart.com/browse/CEEMP-3316) Refactor Collapse to align with new example app structure
- [CEEMP-3317](https://jira.walmart.com/browse/CEEMP-3317) Refactor SeeDetails to align with new example app structure
- [CEEMP-3321](https://jira.walmart.com/browse/CEEMP-3321) Refactor CircularProgressIndicator to align with new example app structure
- [CEEMP-3335](https://jira.walmart.com/browse/CEEMP-3335) Refactor Tag to align with new example app structure
- [CEEMP-3334](https://jira.walmart.com/browse/CEEMP-3334) Refactor StyledText to align with new example app structure
- [CEEMP-3336](https://jira.walmart.com/browse/CEEMP-3336) Refactor Badge to align with new example app structure
- [CEEMP-3332](https://jira.walmart.com/browse/CEEMP-3332) Refactor Spinner to align with new example app structure
- [CEEMP-3331](https://jira.walmart.com/browse/CEEMP-3331) Refactor Popover to align with new example app structure
- [CEEMP-3329](https://jira.walmart.com/browse/CEEMP-3329) Refactor ErrorMessage to align with new example app structure
- [CEEMP-3330](https://jira.walmart.com/browse/CEEMP-3330) Refactor Callout to align with new example app structure
- [CEEMP-3328](https://jira.walmart.com/browse/CEEMP-3328) Refactor SpotIcon to align with new example app structure
- [CEEMP-3327](https://jira.walmart.com/browse/CEEMP-3327) Refactor Alert to align with new example app structure
- [CEEMP-3326](https://jira.walmart.com/browse/CEEMP-3326) Refactor List and List Items to align with new example app structure
- [CEEMP-3323](https://jira.walmart.com/browse/CEEMP-3323) Refactor Modal to align with new example app structure
- [CEEMP-3322](https://jira.walmart.com/browse/CEEMP-3322) Refactor Card to align with new example app structure
- [CEEMP-3325](https://jira.walmart.com/browse/CEEMP-3325) Refactor Divider to align with new example app structure
- [CEEMP-3324](https://jira.walmart.com/browse/CEEMP-3324) Refactor Skeleton to align with new example app structure
- [CEEMP-3318](https://jira.walmart.com/browse/CEEMP-3318) Refactor ProgressIndicator to align with new example app structure
- [CEEMP-3320](https://jira.walmart.com/browse/CEEMP-3320) Refactor Variants to align with new example app structure
- [CEEMP-3311](https://jira.walmart.com/browse/CEEMP-3311) Refactor ChipGroup to align with new example app structure
- [CEEMP-3319](https://jira.walmart.com/browse/CEEMP-3319) Refactor ProgressTracker to align with new example app structure
- (chore) gtp-shared-icons version update
- (chore) Add config file for Codium PR agent
- (chore) Update release strategy to gitflow and update release scripts in hygen
- (chore) Update checkPrdata script
- (chore) Add generate release notes script
- (chore) Update createRelBranch script

## Release 2.2.2-rc.1

- [CEEMP-3426](https://jira.walmart.com/browse/CEEMP-3426) Refresh icons to include SlidersIcon [#593](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/593)
- [CEEMP-3425](https://jira.walmart.com/browse/CEEMP-3425) progressIndicator fixwidth fix [#582](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/582)
- [CEEMP-3401](https://jira.walmart.com/browse/CEEMP-3401) RNModal props are exposed for Modal/BottomSheet/Select [#587](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/587)
- [CEEMP-3395](https://jira.walmart.com/browse/CEEMP-3395) ProgressIndicator render fix [#581](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/581)
- [CEEMP-3439](https://jira.walmart.com/browse/CEEMP-3439) BottomSheet Actions Space issue fix [#586](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/pull/586)

## Release 2.2.2-rc.0

- [CEEMP-3234](https://jira.walmart.com/browse/CEEMP-3234) Feature Request - Add containerStyle to Chips
- [CEEMP-3280](https://jira.walmart.com/browse/CEEMP-3280) Migrate documentation from Styleguidist to Docusaurus
- [CEEMP-3276](https://jira.walmart.com/browse/CEEMP-3276) Select accessibility more props fixes
- [CEEMP-3363](https://jira.walmart.com/browse/CEEMP-3363) Bottomsheet content scroll issue fix
- [CEEMP-3380](https://jira.walmart.com/browse/CEEMP-3380) Feature Request - Add Color prop to Typography components
- [CEEMP-3359](https://jira.walmart.com/browse/CEEMP-3359) Bug Report - nativeID for TextField label
- [CEEMP-3342](https://jira.walmart.com/browse/CEEMP-3342) Feature Request - use native Spinner
- [CEEMP-3254](https://jira.walmart.com/browse/CEEMP-3254) Update LD tokens to latest v0.74

### Internal

- [CEEMP-3314](https://jira.walmart.com/browse/CEEMP-3314) Refactor DateDropdown to align with new example app structure
- [CEEMP-3312](https://jira.walmart.com/browse/CEEMP-3312) Refactor Switch to align with new example app structure
- [CEEMP-3309](https://jira.walmart.com/browse/CEEMP-3309) Refactor Checkbox to align with new example app structure
- [CEEMP-3308](https://jira.walmart.com/browse/CEEMP-3308) Refactor Radio to align with new example app structure
- [CEEMP-3316](https://jira.walmart.com/browse/CEEMP-3316) Refactor Collapse to align with new example app structure
- [CEEMP-3317](https://jira.walmart.com/browse/CEEMP-3317) Refactor SeeDetails to align with new example app structure
- [CEEMP-3321](https://jira.walmart.com/browse/CEEMP-3321) Refactor CircularProgressIndicator to align with new example app structure
- [CEEMP-3335](https://jira.walmart.com/browse/CEEMP-3335) Refactor Tag to align with new example app structure
- [CEEMP-3334](https://jira.walmart.com/browse/CEEMP-3334) Refactor StyledText to align with new example app structure
- [CEEMP-3336](https://jira.walmart.com/browse/CEEMP-3336) Refactor Badge to align with new example app structure
- [CEEMP-3332](https://jira.walmart.com/browse/CEEMP-3332) Refactor Spinner to align with new example app structure
- [CEEMP-3331](https://jira.walmart.com/browse/CEEMP-3331) Refactor Popover to align with new example app structure
- [CEEMP-3329](https://jira.walmart.com/browse/CEEMP-3329) Refactor ErrorMessage to align with new example app structure
- [CEEMP-3330](https://jira.walmart.com/browse/CEEMP-3330) Refactor Callout to align with new example app structure
- [CEEMP-3328](https://jira.walmart.com/browse/CEEMP-3328) Refactor SpotIcon to align with new example app structure
- [CEEMP-3327](https://jira.walmart.com/browse/CEEMP-3327) Refactor Alert to align with new example app structure
- [CEEMP-3326](https://jira.walmart.com/browse/CEEMP-3326) Refactor List and List Items to align with new example app structure
- [CEEMP-3323](https://jira.walmart.com/browse/CEEMP-3323) Refactor Modal to align with new example app structure
- [CEEMP-3322](https://jira.walmart.com/browse/CEEMP-3322) Refactor Card to align with new example app structure
- [CEEMP-3325](https://jira.walmart.com/browse/CEEMP-3325) Refactor Divider to align with new example app structure
- [CEEMP-3324](https://jira.walmart.com/browse/CEEMP-3324) Refactor Skeleton to align with new example app structure
- [CEEMP-3318](https://jira.walmart.com/browse/CEEMP-3318) Refactor ProgressIndicator to align with new example app structure
- [CEEMP-3320](https://jira.walmart.com/browse/CEEMP-3320) Refactor Variants to align with new example app structure
- [CEEMP-3311](https://jira.walmart.com/browse/CEEMP-3311) Refactor ChipGroup to align with new example app structure
- [CEEMP-3319](https://jira.walmart.com/browse/CEEMP-3319) Refactor ProgressTracker to align with new example app structure
- (chore) gtp-shared-icons version update
- (chore) Add config file for Codium PR agent
- (chore) Update release strategy to gitflow and update release scripts in hygen
- (chore) Update checkPrdata script
- (chore) Add generate release notes script
- (chore) Update createRelBranch script

## Release 2.2.1

- [CEEMP-3364](https://jira.walmart.com/browse/CEEMP-3364) Bug Report - BottomSheet freezing UI
- (chore) update gtp-shared-icons version 1.0.8
- (chore) update release scripts to create release branch
- [CEEMP-3344](https://jira.walmart.com/browse/CEEMP-3344) Bug Report - Multi Select language issue
- [CEEMP-3279](https://jira.walmart.com/browse/CEEMP-3279) Bug Report - CheckBox Talkback announce twice
- [CEEMP-3256](https://jira.walmart.com/browse/CEEMP-3256) Bug Report - TextField accessibility issue
- [CEEMP-3306](https://jira.walmart.com/browse/CEEMP-3306) Bug Report - maxLength prop in TextField
- [CEEMP-3360](https://jira.walmart.com/browse/CEEMP-3360) Bug Report - Replace verticalAlign styleProps
- [CEEMP-3277](https://jira.walmart.com/browse/CEEMP-3277) Bug Report - BottomSheet action button issue
- [CEEMP-3297](https://jira.walmart.com/browse/CEEMP-3297) Bug Report - SeeDetails style issue 2.1.9
- [CEEMP-3391](https://jira.walmart.com/browse/CEEMP-3391) Export All component props
- [CEEMP-3274](https://jira.walmart.com/browse/CEEMP-3274) Add new Associate experience(AX) components Filter and FilterGroup
- [CEEMP-3198](https://jira.walmart.com/browse/CEEMP-3198) Refactor legacy component: Collapse & SeeDetails
- [CEEMP-3233](https://jira.walmart.com/browse/CEEMP-3233) Enable NativeDriver in Spinner
- [CEEMP-3288](https://jira.walmart.com/browse/CEEMP-3288) Add useAccessibilityFocus hook
- [CEEMP-3194](https://jira.walmart.com/browse/CEEMP-3194) Refactor legacy component: DateDropdown
- [CEEMP-3356](https://jira.walmart.com/browse/CEEMP-3356) Select component with extra content option for single option
- [CEEMP-3280](https://jira.walmart.com/browse/CEEMP-3280) Parse Components and generate mdx in new docs Docusaurus
- [CEEMP-3375](https://jira.walmart.com/browse/CEEMP-3375) Add Utilities in new docs Docusaurus
- [CEEMP-3372](https://jira.walmart.com/browse/CEEMP-3372) Add gtp-shared-icons in new docs Docusaurus
- [CEEMP-3371](https://jira.walmart.com/browse/CEEMP-3371) Add Colors Palette in new docs Docusaurus
- [CEEMP-3296](https://jira.walmart.com/browse/CEEMP-3296) (internal) Refactor example app - refactor to new HomeScreen

### Breaking changes

- Starting with this release, we have Refactored the legacy components bulleted below.(aligned to current coding standards). In this process, we deprecated the prop `style` and now its called `UNSAFE_style`
  - DateDropdown
  - Collapse
  - SeeDetails

**Before:**

```js static noeditor
import {Collapse, SeeDetails} from '@walmart/gtp-shared-components';

 <Collapse style={styles.normal}>something</Collapse>
 <SeeDetails style={styles.normal}>something</SeeDetails>
```

**after**

```js static noeditor
import {Collapse, SeeDetails} from '@walmart/gtp-shared-components';

  <Collapse UNSAFE_style={styles.normal}>something</Collapse>
  <SeeDetails UNSAFE_style={styles.normal}>something</SeeDetails>
```

## Release 2.2.1-rc.1

- [CEEMP-3364](https://jira.walmart.com/browse/CEEMP-3364) Bug Report - BottomSheet freezing UI

## Release 2.2.1-rc.0

- (chore) update gtp-shared-icons version 1.0.8
- (chore) update release scripts to create release branch
- [CEEMP-3344](https://jira.walmart.com/browse/CEEMP-3344) Bug Report - Multi Select language issue
- [CEEMP-3279](https://jira.walmart.com/browse/CEEMP-3279) Bug Report - CheckBox Talkback announce twice
- [CEEMP-3256](https://jira.walmart.com/browse/CEEMP-3256) Bug Report - TextField accessibility issue
- [CEEMP-3306](https://jira.walmart.com/browse/CEEMP-3306) Bug Report - maxLength prop in TextField
- [CEEMP-3360](https://jira.walmart.com/browse/CEEMP-3360) Bug Report - Replace verticalAlign styleProps
- [CEEMP-3277](https://jira.walmart.com/browse/CEEMP-3277) Bug Report - BottomSheet action button issue
- [CEEMP-3297](https://jira.walmart.com/browse/CEEMP-3297) Bug Report - SeeDetails style issue 2.1.9
- [CEEMP-3391](https://jira.walmart.com/browse/CEEMP-3391) Export All component props
- [CEEMP-3274](https://jira.walmart.com/browse/CEEMP-3274) Add new Associate experience(AX) components Filter and FilterGroup
- [CEEMP-3198](https://jira.walmart.com/browse/CEEMP-3198) Refactor legacy component: Collapse & SeeDetails
- [CEEMP-3233](https://jira.walmart.com/browse/CEEMP-3233) Enable NativeDriver in Spinner
- [CEEMP-3288](https://jira.walmart.com/browse/CEEMP-3288) Add useAccessibilityFocus hook
- [CEEMP-3194](https://jira.walmart.com/browse/CEEMP-3194) Refactor legacy component: DateDropdown
- [CEEMP-3356](https://jira.walmart.com/browse/CEEMP-3356) Select component with extra content option for single option
- [CEEMP-3280](https://jira.walmart.com/browse/CEEMP-3280) Parse Components and generate mdx in new docs Docusaurus
- [CEEMP-3375](https://jira.walmart.com/browse/CEEMP-3375) Add Utilities in new docs Docusaurus
- [CEEMP-3372](https://jira.walmart.com/browse/CEEMP-3372) Add gtp-shared-icons in new docs Docusaurus
- [CEEMP-3371](https://jira.walmart.com/browse/CEEMP-3371) Add Colors Palette in new docs Docusaurus
- [CEEMP-3296](https://jira.walmart.com/browse/CEEMP-3296) (internal) Refactor example app - refactor to new HomeScreen

### Breaking changes

- Starting with this release, we have Refactored the legacy components bulleted below.(aligned to current coding standards). In this process, we deprecated the prop `style` and now its called `UNSAFE_style`
  - DateDropdown
  - Collapse
  - SeeDetails

**Before:**

```js static noeditor
import {Collapse, SeeDetails} from '@walmart/gtp-shared-components';

 <Collapse style={styles.normal}>something</Collapse>
 <SeeDetails style={styles.normal}>something</SeeDetails>
```

**after**

```js static noeditor
import {Collapse, SeeDetails} from '@walmart/gtp-shared-components';

  <Collapse UNSAFE_style={styles.normal}>something</Collapse>
  <SeeDetails UNSAFE_style={styles.normal}>something</SeeDetails>
```

## Release 2.2.0

- PLEASE IGNORE THIS RELEASE. DO NOT INSTALL.

## Release 2.1.10

- [CEEMP-3198](https://jira.walmart.com/browse/CEEMP-3198) Restore legacy component: Collapse & SeeDetails
- [CEEMP-3298](https://jira.walmart.com/browse/CEEMP-3298) Bug Report: Modal ButtonsGroup issue 2.1.9
- [CEEMP-3228](https://jira.walmart.com/browse/CEEMP-3228) (internal) Styleguidist to Docusaurus POC
- [CEEMP-3289](https://jira.walmart.com/browse/CEEMP-3289) (internal) Refactor example app - align naming of the screens with BLS (change from plural to singular)
- [CEEMP-3291](https://jira.walmart.com/browse/CEEMP-3291) (internal) Refactor example app - rename screens to be consistent
- [CEEMP-3293](https://jira.walmart.com/browse/CEEMP-3293) (internal) Refactor example app - group recipes by component
- [CEEMP-3295](https://jira.walmart.com/browse/CEEMP-3295) (internal) Refactor example app - rename components screens
- (chore) remove engines in package.json

## Release 2.1.9

- [CEEMP-3206](https://jira.walmart.com/browse/CEEMP-3206) (chore) upgrade shared-components library to 0.72.x
- [CEEMP-3198](https://jira.walmart.com/browse/CEEMP-3198) Refactor legacy component: Collapse & SeeDetails
- [CEEMP-3196](https://jira.walmart.com/browse/CEEMP-3196) Refactor legacy component: CircularProgressIndicator
- [CEEMP-3263](https://jira.walmart.com/browse/CEEMP-3263) BottomSheet and Modal x icon accessibilityLabel update
- [CEEMP-3261](https://jira.walmart.com/browse/CEEMP-3261) TextField paddingVertical update
- [CEEMP-3258](https://jira.walmart.com/browse/CEEMP-3258) Fix button flickering issue
- (chore) Re-enable eslint import order
- (chore) Remove storybook

## Release 2.1.8

- [CEEMP-3257](https://jira.walmart.com/browse/CEEMP-3257) Bug Report - Tag not allowing accessibility props
- [CEEMP-3203](https://jira.walmart.com/browse/CEEMP-3203) Bug Report - ButtonGroup not fitting in Modal
- [CEEMP-3255](https://jira.walmart.com/browse/CEEMP-3255) (internal) update tokens scripts with the new dir structure
- [CEEMP-3245](https://jira.walmart.com/browse/CEEMP-3245) (internal) add README.dependencies.md
- [CEEMP-3246](https://jira.walmart.com/browse/CEEMP-3246) (internal) port hygen templating from BLS -> LD

### Deprecated

- [CEEMP-3195](https://jira.walmart.com/browse/CEEMP-3195) [GTP-LD] deprecated legacy component: Scrollbar
- [CEEMP-3197](https://jira.walmart.com/browse/CEEMP-3197) [GTP-LD] deprecated legacy component: Carousel

## Release 2.1.7

- [CEEMP-3222](https://jira.walmart.com/browse/CEEMP-3222) [GTP-LD] Bug Report - Alert announcement in accessibility
- [CEEMP-3226](https://jira.walmart.com/browse/CEEMP-3226) [GTP-LD] Migrate NPM Dist Tags
- [CEEMP-3230](https://jira.walmart.com/browse/CEEMP-3230) [GTP-LD] Bug Report - Tab Navigation portrait-to-landscape issue
- [CEEMP-3202](https://jira.walmart.com/browse/CEEMP-3202) [GTP-LD] Bug Report - Select Talkback announce other accessibility props
- [CEEMP-3221](https://jira.walmart.com/browse/CEEMP-3221) (chore, internal) Rename local variables from local*\* to *\*
- (chore) align node version with the on in allspark

## Release 2.1.6

- (chore) refactor TS typing in colors.ts
- (docs) add docstrings in colorUtils.ts
- [CEEMP-3210](https://jira.walmart.com/browse/CEEMP-3210) Bug Report - Bottom sheet Title padding
- [CEEMP-3148](https://jira.walmart.com/browse/CEEMP-3148) Bug Report - Select overlay issue
- [CEEMP-3187](https://jira.walmart.com/browse/CEEMP-3187) Bug Report - Select component Gap on card
- [CEEMP-3215](https://jira.walmart.com/browse/CEEMP-3215) (chore, internal) - Automate and move NPM publishing to Looper
- [CEEMP-3236](https://jira.walmart.com/browse/CEEMP-3236) Bug Report - Bottom sheet x button hitslop center alignment issue
- (docs, internal) fix looper links in publishing docs.

## Release 2.1.5

- [CEEMP-3125](https://jira.walmart.com/browse/CEEMP-3125) Bug Report - TextField,Select Checkbox Toggle update issue
- [CEEMP-3205](https://jira.walmart.com/browse/CEEMP-3205) Bug Report - TextField cursor moving unexpectedly
- [CEEMP-3183](https://jira.walmart.com/browse/CEEMP-3183) Feature Request - forwardRef in Button
- [CEEMP-3192](https://jira.walmart.com/browse/CEEMP-3192) Feature Request - Banner left icon and icon color

## Release 2.1.4

- [CEEMP-3191](https://jira.walmart.com/browse/CEEMP-3191) Feature Request - Snackbar Change Close button Accessibility role to "button"
- [CEEMP-3181](https://jira.walmart.com/browse/CEEMP-3181) Bug Report - BottomSheet footer margin should be removed
- (chore, internal) Include Sonar status in README.md

## Release 2.1.3

- [CEEMP-3133](https://jira.walmart.com/browse/CEEMP-3133) Bug Report - Switch component label/state accessability
- [CEEMP-3164](https://jira.walmart.com/browse/CEEMP-3164) Feature Request - addSnack hook accessibility props
- [CEEMP-3171](https://jira.walmart.com/browse/CEEMP-3171) Bug Report - TextField/Select alignment issues
- [CEEMP-3067](https://jira.walmart.com/browse/CEEMP-3067) Bug Report - Select styling issue
- [CEEMP-3173](https://jira.walmart.com/browse/CEEMP-3173) VoiceOver/Talkback TabNavigation Accessibility role and state are not read
- [CEEMP-3153](https://jira.walmart.com/browse/CEEMP-3153) Add dummy import for colors.json
- [CEEMP-3033](https://jira.walmart.com/browse/CEEMP-3033) Add Colors section to LDRNExample

## Release 2.1.2

- [CEEMP-3091](https://jira.walmart.com/browse/CEEMP-3091) Bug Report - Android accessibility issue Item Info team
- [CEEMP-3132](https://jira.walmart.com/browse/CEEMP-3132) Update Tag component docs + examples
- [CEEMP-3138](https://jira.walmart.com/browse/CEEMP-3138) Bug Report - TextArea disabled text should be grey
- [CEEMP-3153](https://jira.walmart.com/browse/CEEMP-3153) Refactor imports of colors.json with LD globals token
- [CEEMP-3155](https://jira.walmart.com/browse/CEEMP-3155) Bug Report - Menu elevation doesn't match LD specs

## Release 2.1.1

- [CEEMP-3110](https://jira.walmart.com/browse/CEEMP-3110) Bug Report - Select and TextField component label style issue
- [CEEMP-3121](https://jira.walmart.com/browse/CEEMP-3121) Bug Report - Alert horizontal margin

## Release 2.1.0

- [CEEMP-3066](https://jira.walmart.com/browse/CEEMP-3066) Bug Report - animation issue in Snackbar Android
- [CEEMP-3096](https://jira.walmart.com/browse/CEEMP-3096) Bug Report - Popover - shadow not showing in Android
- [CEEMP-3102](https://jira.walmart.com/browse/CEEMP-3102) Bug Report - Modal styling issue
- [CEEMP-3105](https://jira.walmart.com/browse/CEEMP-3105) Bug Report - BottomSheet expose onOpened prop
- [CEEMP-3109](https://jira.walmart.com/browse/CEEMP-3109) change bundle name (iOS) for LDRNExample
- [CEEMP-3115](https://jira.walmart.com/browse/CEEMP-3115) add signing for in-house distribution of LDRNExample

## Breaking changes

- Starting with this release, we have added a new peerDependency that you will need to add to your app:
  ```json static noeditor
  yarn add react-native-drop-shadow
  ```

## Release 2.0.10

- [CEEMP-2987](https://jira.walmart.com/browse/CEEMP-2987) Bug Report - Select gap on Android
- [CEEMP-3101](https://jira.walmart.com/browse/CEEMP-3101) Styleguidist docs fails after PR #405
- [CEEMP-3100](https://jira.walmart.com/browse/CEEMP-3100) Bug Report - postinstall script fails on Windows
- [CEEMP-3072](https://jira.walmart.com/browse/CEEMP-3072) Fix BottomSheet Keyboard Scrolling
- [CEEMP-3079](https://jira.walmart.com/browse/CEEMP-3079) Feature Request - Collapse customize font and arrow size
- [CEEMP-3088](https://jira.walmart.com/browse/CEEMP-3088) Bug Report - TabNavigation example screen

### Breaking changes

- Starting with this release, we have added a new peerDependency that you will need to add to your app:
  ```json static noeditor
  yarn add react-native-device-info
  ```

## Release 2.0.9

- [CEEMP-3070](https://jira.walmart.com/browse/CEEMP-3070) Bug Report - Bottomsheet divider issue
- [CEEMP-3076](https://jira.walmart.com/browse/CEEMP-3076) Bug Report - TabNavigationItem flickering issue and example app updated
- [CEEMP-3068](https://jira.walmart.com/browse/CEEMP-3068) Add TestId to TabNavigationItem Component
- [CEEMP-3063](https://jira.walmart.com/browse/CEEMP-3063) Enable SonarQube Decoration in PR, Looper

## Release 2.0.8

- [CEEMP-2995](https://jira.walmart.com/browse/CEEMP-2995) Bug Report - TabNavigation Badge font and alignment
- [CEEMP-3049](https://jira.walmart.com/browse/CEEMP-3049) Bug report - Chip, ChipGroup styling issues
- [CEEMP-3029](https://jira.walmart.com/browse/CEEMP-3029) Bug Report - Select close on backdrop press

## Release 2.0.7

- [CEEMP-3034](https://jira.walmart.com/browse/CEEMP-3034) Upgrade gtp-shared-icons to latest version 1.0.7
- [CEEMP-3001](https://jira.walmart.com/browse/CEEMP-3001) Bug Report - Checkbox, Radio button accessibility override
- [CEEMP-3035](https://jira.walmart.com/browse/CEEMP-3035) Bug Report - SpotIcon color change
- [CEEMP-3039](https://jira.walmart.com/browse/CEEMP-3039) Bug Report - need a way to remove bottom sheet paddings or margins
- [CEEMP-3040](https://jira.walmart.com/browse/CEEMP-3040) Feature Request - useSnackbar documentation correction
- [CEEMP-3036](https://jira.walmart.com/browse/CEEMP-3036) Bug Report - BottomSheet close button

## Release 2.0.6

- [CEEMP-3024](https://jira.walmart.com/browse/CEEMP-3024) Bug Report - BottomSheet with ScrollView content
- [CEEMP-3028](https://jira.walmart.com/browse/CEEMP-3028) Tab navigation width issue
- [CEEMP-3000](https://jira.walmart.com/browse/CEEMP-3000) Bug Report - Button leading icon styling
- [CEEMP-2987](https://jira.walmart.com/browse/CEEMP-2987) Bug Report - Select gap on Android
- [CEEMP-2991](https://jira.walmart.com/browse/CEEMP-2991) Bug report - ButtonGroup cannot be forced to full width
- [CEEMP-2943](https://jira.walmart.com/browse/CEEMP-2943) Bug Report - Select infinite loop when onChange contains hook call
- [CEEMP-2841](https://jira.walmart.com/browse/CEEMP-2841) (chore) update to the latest LD tokens version
- [CEEMP-3020](https://jira.walmart.com/browse/CEEMP-3020) (chore) Upgrade root library to react-native 0.70.8
- [CEEMP-2726](https://jira.walmart.com/browse/CEEMP-2726) (chore) Upgrade example app to use react-native 0.70.8
- [CEEMP-3025](https://jira.walmart.com/browse/CEEMP-3025) Bug Report - icon placement with 'trailing' prop for full width primary button
- [CEEMP-3027](https://jira.walmart.com/browse/CEEMP-3027) (internal) - change iconset for the example app

## Release 2.0.5

- [CEEMP-2741](https://jira.walmart.com/browse/CEEMP-2741) Feature Request - Refactor SpinnerOverlay
- [CEEMP-2876](https://jira.walmart.com/browse/CEEMP-2876) Select Modal/Bottomsheet showing empty space when no title
- [CEEMP-2930](https://jira.walmart.com/browse/CEEMP-2930) Bug Report - Switch animation on Android
- [CEEMP-2843](https://jira.walmart.com/browse/CEEMP-2843) (internal) fix Props and Methods section in docs for Missed Components
- [CEEMP-2829](https://jira.walmart.com/browse/CEEMP-2929) Bug Report - Select styling and testability

## Release 2.0.4

- [CEEMP-2874](https://jira.walmart.com/browse/CEEMP-2874) Bug Report - Button with long title
- [CEEMP-2883](https://jira.walmart.com/browse/CEEMP-2883) Bug Report - Snackbar close button pass empty onClose
- [CEEMP-2933](https://jira.walmart.com/browse/CEEMP-2933) Feature Request - BottomSheet Android back button
- [CEEMP-2875](https://jira.walmart.com/browse/CEEMP-2875) Bug Report - BottomSheet visual issues
- [CEEMP-2847](https://jira.walmart.com/browse/CEEMP-2847) Feature Request - Metric, allow more than one metric

## Release 2.0.3

- [CEEMP-2864](https://jira.walmart.com/browse/CEEMP-2864) Bug Report - TextField Android dark mode
- [CEEMP-2872](https://jira.walmart.com/browse/CEEMP-2872) Bug Report - TextField onBlur override
- [CEEMP-2861](https://jira.walmart.com/browse/CEEMP-2861) Feature Request - Button styling customization
- [CEEMP-2873](https://jira.walmart.com/browse/CEEMP-2873) BottomSheet divider styling
- [CEEMP-2864](https://jira.walmart.com/browse/CEEMP-2864), [CEEMP-2880](https://jira.walmart.com/browse/CEEMP-2880) Bug Report - TextField Android dark mode
- [CEEMP-2879](https://jira.walmart.com/browse/CEEMP-2879) (chore, internal) rename package.json script and add step to Looper
- [CEEMP-2871](https://jira.walmart.com/browse/CEEMP-2871) (docs) update docs to reflect the latest stable release
- [CEEMP-2867](https://jira.walmart.com/browse/CEEMP-2867) (chore, internal) fix colors imports in embedded example app

## Release 2.0.2

- [CEEMP-2854](https://jira.walmart.com/browse/CEEMP-2854) Bug Report - ChipGroup infinite loop
- [CEEMP-2845](https://jira.walmart.com/browse/CEEMP-2845) Bug Report - Modal close button, background on some Android devices, Progress tracker item text line height
- [CEEMP-2853](https://jira.walmart.com/browse/CEEMP-2853) Bug Report - BottomSheet unable to load section list data
- [CEEMP-2856](https://jira.walmart.com/browse/CEEMP-2856) Bug Report - BottomSheet layout when keyboard is up
- [RTASPE-7751](https://jira.walmart.com/browse/RTASPE-7751) Print bottom sheet select label blanks out background

## Release 2.0.1

- [CEEMP-2860](https://jira.walmart.com/browse/CEEMP-2860) Bug Report - Modal, improper spacing and wrong font
- [CEEMP-2857](https://jira.walmart.com/browse/CEEMP-2857) Bug Report - BottomSheet with Select issues
- [CEEMP-2855](https://jira.walmart.com/browse/CEEMP-2855) Bug Report - MinusIcon, PlusIcon styling
- [CEEMP-2852](https://jira.walmart.com/browse/CEEMP-2852) Bug Report - Modal, improper title wrapping for long text
- [CEEMP-2851](https://jira.walmart.com/browse/CEEMP-2851) Bug Report - BottomSheet with TextInput dismiss
- [CEEMP-2844](https://jira.walmart.com/browse/CEEMP-2844) Bug Report - Alert action button position does not match LD
- [CEEMP-2842](https://jira.walmart.com/browse/CEEMP-2842) Bug Report - ChipGroup (single selection)
- [CEEMP-2840](https://jira.walmart.com/browse/CEEMP-2840) Bug Report - TabNavigation children not showing
- [CEEMP-2765](https://jira.walmart.com/browse/CEEMP-2765) Bug Report - Extra space at bottom of BottomSheet

## Release 2.0.0

### Overview

This release is the result of a major refactoring effort. The entire codebase has been re-written from the ground up, targeting the following characteristics:

- full alignment with the latest Living Design (LD) design specs (aka LD3)
- full alignment with modern React Native constructs (e.g. Functional Components instead of Classes), hooks, strong typing
- simplified styling, eliminate the convoluted theme-ing system which in effect allowed a complete re-styling of components, defeating the purpose of a Design System.
- simplified importing - everything is now exposed in the root, no more drilling down into the dist directory
- alignment of API with the Web implementation of LD
- separation of the icons into a separate repo to improve maintainability
- usage of dynamic LD tokens for all styling props (imported from livingdesign/tokens)
- alignment of project structure to current industry best practices
- comprehensive unit tests for all components - unit tests were virtually inexistent before

The new structure of the library allows us to continue to support previous versions of the components (grouped as `legacy` throughout the docs).
These co-exist side-by-side with the re-written components (grouped as `next` in the docs). They are marked as deprecated meaning, they will appear with a strikethrough font in the docs and also in the code if you use eslint, prettier, typescript.

For cases where the old names of the component (legacy) clashes with the new name (next), only the new component is present, but the API (props set) will support all the old props for backwards compatibility. Caveat emptor here: many of these props have no effect, and in the docs we give you what to use instead from the new API set.

The new build system also allow us to continue to release `legacy` versions independently for consumers who are still using those versions. The version semver structure will be frozen at `1.8` (current latest version there is `1.8.18`), meaning there will be no more feature development on that track, just occasional bug fixes as needed, hence all future releases (if any) will be patch releases (`1.8.*`)

To assist you with the migration we are providing a series of `codemods` scripts which automate various changes in your codebase. See [Migration using codemods](#migration-using-codemods) section below.

Here are the full details of the changes:

### Breaking changes

- `TransparentIconButton` has been deprecated and removed from the library. Please use IconButton instead.

  **Change from:**

  ```js static noeditor
  import {TransparentIconButton} from '@walmart/gtp-shared-components';
  import {CloseIcon} from '@walmart/gtp-shared-components';

  <TransparentIconButton small icon={<CloseIcon />} onPress={() => {}} />;
  ```

  **To:**

  ```js static noeditor
  import {IconButton, Icons} from '@walmart/gtp-shared-components';

  <IconButton size="small" children={<Icons.Close />} onPress={() => {}} />;
  ```

- `IconButton` has a different set of props
  - `type` has been deprecated and has no effect
  - `icon` has been deprecated. Use `children` instead.
- `Spinner` has a different set of props
  - `small` has been deprecated and has not effect. Use `size="small"` instead
  - `color` takes only 2 values 'white' or 'gray'
- `Body` redesigned + different props. See documentation.
- `Caption` different props. See documentation.
- `Display` redesigned + different props. See documentation.
- `Alert` redesigned + different props. See documentation.
- `Badge` redesigned + different props. See documentation.
- `TextField` redesigned + different props. See documentation.
- `List` has a different set of props.
  - `items` has been deprecated. Use `children` instead See documentation.
- `ProgressTracker` redesigned + different props. See documentation.
- `Skeleton` has a different set of props. See documentation.
  - `rounded` has been deprecated and replaced with `variant`
  - `lines` has been deprecated and replaced with `SkeletonText`
  - `animator` has been deprecated and has no effect
  - the static method `createAnimator()` has been removed and is a breaking change

### Changed

#### Alignment with LD3 specs

We have re-structured the documentation in 2 sections:

- `Components` this is where the refactored components are documented
- `Components - LEGACY` this is where all the previous version of components that are documented. They appear in ~~strikethrough~~ and a deprecation message is present (with a hint of what to use instead)

- The following components have been `refactored/LD3 aligned` and are available in this release:

  - Alert - same name, redesigned + different props
  - Badge - same name, redesigned + different props
  - Banner - new
  - Body - same name, redesigned + different props
  - BottomSheet - same name, same design, different props
  - Button - new
  - ButtonGroup - new
  - Caption - same name, redesigned + different props
  - Card - new
  - CardHeader - new
  - CardMedia - new
  - CardContent - new
  - CardActions - new
  - Checkbox - new
  - Chip - new
  - ChipGroup - new
  - CircularProgressIndicator - same name, redesigned
  - DataTable - new
  - DataTableBody - new
  - DataTableBulkActions - new
  - DataTableCell - new
  - DataTableCellActions - new
  - DataTableCellActionsMenu - new
  - DataTableCellSelect - new
  - DataTableCellStatus - new
  - DataTableHead - new
  - DataTableHeader - new
  - DataTableHeaderSelect - new
  - DataTableRow - new
  - Display - same name, redesigned + different props
  - ErrorMessage - new
  - FormGroup - new
  - Heading - new
  - IconButton - same name, redesigned + different props
  - Link - new
  - List - existing, new props
  - ListItem - new
  - LivingDesignProvider - new
  - Menu - new
  - MenuItem - new
  - Metric - new
  - Modal - new
  - Nudge - new
  - Popover - new
  - ProgressIndicator - new
  - ProgressTracker - same name, redesigned + different props
  - ProgressTrackerItem - same name, redesigned + different props
  - Radio - new
  - Rating - new
  - Select - new (replaces Dropdown)
  - Segmented - same name, redesigned + different props
  - Segment - new
  - Skeleton - same name, different props
  - SkeletonText - new
  - Spinner - same name, different props
  - SpinnerOverlay - same name, new props
  - SpotIcon - new
  - StyledText - new
  - Switch - new
  - TabNavigation - new
  - TabNavigationItem - new
  - Tag - new
  - TextArea - same name, redesigned + different props
  - TextField - same name, redesigned + different props
  - Variants
  - useSnackbar - new (used together with LivingDesignProvider)
  - WizardFooter - new

- The following components are being `deprecated`, i.e. they are still available in the library, but will be removed in a future release.
  Ample amount of time will be provided before that to allow you to change your code. We will also provide assistance with your migration as needed.

  - PrimaryButton - use Button variant="primary" instead
  - SecondaryButton - use Button variant="secondary" instead
  - TertiaryButton - use Button variant="tertiary" instead
  - TransparentButton - use Button variant="transparent" instead
  - DestructiveButton - use Button variant="destructive" instead
  - BannerButton - not present in LD3 specs
  - PovPrimaryButton - not present in LD3 specs
  - PovSecondaryButton - not present in LD3 specs
  - LinkButton - use Link instead
  - Chips - use ChipGroup instead
  - Snackbar - use LivingDesignProvider/SnackbarProvider + useSnackbar instead
  - AlertError - use Banner variant="error" instead
  - AlertInfo - use Banner variant="info" instead
  - AlertInfo2 - use Banner variant="info" instead
  - AlertInfo3 - use Banner variant="info" instead
  - MessageError - use Alert variant="error" instead
  - MessageSuccess - use Alert variant="success" instead
  - MessageWarning - use Alert variant="warning" instead
  - Body2 - use Body instead
  - Caption2 - use Caption instead
  - Headline - use Heading instead
  - Price - use Body isMonospace={true} instead
  - Subheader - use Heading instead
  - Subheader2 - use Heading instead
  - Title - use Heading instead
  - Title2 - use Heading instead
  - Title3 - use Heading instead
  - AvailabilityBadge - use Badge instead
  - CountBadge - use Badge instead
  - InformationalBadge - use Badge instead
  - MediaBadge - use Badge instead
  - SolidCard - use Card instead
  - OutlineCard - use Card instead
  - MediaCard - use Card instead
  - ThemeProvider - use LivingDesignProvider instead
  - SupportiveText - use StyledText instead
  - MoneyCircleFillIcon - not present in LD3 specs
  - PlayCircleIcon - not present in LD3 specs
  - ReorderIcon - not present in LD3 specs
  - ReorderFillIcon - not present in LD3 specs
  - Icon - not present in LD3 specs
  - ShuffleIcon - not present in LD3 specs
  - StoreFillIcon - not present in LD3 specs
  - CheckboxItem - use Checkbox instead
  - CheckboxItemGroup - use FormGroup instead
  - Flag - use Tag instead
  - PrimaryTag - use Tag instead
  - SecondaryTag - use Tag instead
  - TertiaryTag - use Tag instead
  - RollbackFlag - use Tag instead
  - FilledFlag - use Tag instead
  - RadioItem - use Radio instead
  - RadioItemGroup - use FormGroup instead
  - ToggleItem - use Switch instead
  - ToggleItemGroup - use FormGroup instead
  - CardOverlay - use Modal instead
  - Overlay - use Modal instead
  - Ratings - use Rating instead
  - MultiLineTextField - use TextField instead
  - PasswordField - use TextField instead
  - Dropdown - use Select instead

  The deprecated components are marked clearly as **~~Deprecated~~** in the docs.

  See the [latest docs](https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/#/Introduction) for the up-to-date list of next / legacy components.

#### Imports

- All imports have been simplified so that now you can import from root instead of `dist`.
  No more drilling down into the dist directory to find the location of what you need to import.

  Here are some examples:

  **Example 1:**

  **Before:**

  ```js static noeditor
  import colors from '@walmart/gtp-shared-components/dist/theme/colors.json';
  import IconButton from '@walmart/gtp-shared-components/dist/buttons/icon-button';
  ```

  **After:**

  ```js static noeditor
  import {colors, IconButton} from '@walmart/gtp-shared-components';
  ```

  **Example 2:**

  **Before:**

  ```js static noeditor
  import colors from '@walmart/gtp-shared-components/dist/theme/colors.json';
  import PlusIcon from '@walmart/gtp-shared-components/dist/icons/plus-icon';
  import BoxIcon from '@walmart/gtp-shared-components/dist/icons/box-icon';
  // used in the code like this:
  <PlusIcon {...props} />
  <BoxIcon {...props} />
  ```

  **After:**

  ```js static noeditor
  import {colors, Icons} from `@walmart/gtp-shared-components`
  // and then, use them in the code like this:
  <Icons.PlusIcon {...props} />
  <Icons.BoxIcon {...props} />
  // all the rest of the code stays the same
  ```

  **Example 3:**

  **Before:**

  ```js static noeditor
  import {
    Dropdown,
    TextArea,
    TextField,
  } from '@walmart/gtp-shared-components/dist/form';
  import {Body, Caption} from '@walmart/gtp-shared-components/dist/typography';
  import EmailIcon from '@walmart/gtp-shared-components/dist/icons/email-icon';
  import InfoCircleIcon from '@walmart/gtp-shared-components/dist/icons/info-circle-icon';
  import DateDropdown from '@walmart/gtp-shared-components/dist/form/dropdowns/date-dropdown';
  import RadioItem from '@walmart/gtp-shared-components/dist/form/toggleable/radio-item';
  import Segmented from '@walmart/gtp-shared-components/dist/form/toggleable/segmented';
  import ToggleItem from '@walmart/gtp-shared-components/dist/form/toggleable/toggle-item';
  import colors from '@walmart/gtp-shared-components/dist/theme/colors.json';
  // and used in the code like this:
  <EmailIcon {...props} />
  <InfoCircleIcon {...props} />
  ```

  **After:**

  ```js static noeditor
  import {
    colors,
    Body,
    Caption,
    Dropdown,
    DateDropdown,
    Icons,
    RadioItem,
    Segmented
    TextArea,
    TextField,
    ToggleItem,
  } from '@walmart/gtp-shared-components';
  // and then, use in the code like this:
  <Icons.EmailIcon {...props} />
  <Icons.InfoCircleIcon {...props} />
  // all the rest of the code stays the same
  ```

#### Other examples of before / after the upgrade

**Example 4:**

**Before:**

```js static noeditor
import {List} from '@walmart/gtp-shared-components';
const item=[
  {
  title: 'Pressable List Item Title 1',
  content:'Get it shipped to your door',
  leading: <Icons.InfoCircleIcon size={24} />,
  trailing: <Icons.CheckIcon size={24} />,
  onPress: () => {
    console.log('Pressed!');
  },
}];
<List items={item}>
```

**After:**

```js static noeditor
import {
  List,
  ListItem,
  Icons,
  IconButton,
} from '@walmart/gtp-shared-components';

<List>
  <ListItem
    title="Pressable List Item Title 1"
    leading={<Icons.InfoCircleIcon size={24} />}
    trailing={
      <IconButton
        size={24}
        onPress={() => {
          console.log('Pressed!');
        }}
      />
    }>
    Get it shipped to your door
  </ListItem>
</List>;
```

**Example 5:**

**Before:**

```js static noeditor
import {ProgressTracker} from '@walmart/gtp-shared-components';
<ProgressTracker
  stepCount={5}
  completeCount={3}
  labels={['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5']}
/>;
```

**After:**

```js static noeditor
import {
  ProgressTracker,
  ProgressTrackerItem,
} from '@walmart/gtp-shared-components';

<ProgressTracker activeIndex={2} variant="info">
  <ProgressTrackerItem>Step 1</ProgressTrackerItem>
  <ProgressTrackerItem>Step 2</ProgressTrackerItem>
  <ProgressTrackerItem>Step 3</ProgressTrackerItem>
  <ProgressTrackerItem>Step 4</ProgressTrackerItem>
</ProgressTracker>;
```

**Example 6:**

**Before:**

```js static noeditor
import {Segmented, Segment} from '@walmart/gtp-shared-components';
<Controller controlProp="selectedIndex">
  <Segmented
    segments={[
      <Segmented.Segment>First</Segmented.Segment>,
      <Segmented.Segment>Second</Segmented.Segment>,
      <Segmented.Segment>Third</Segmented.Segment>,
    ]}
  />
</Controller>;
```

**After:**

```js static noeditor
import {Segmented, Segment} from '@walmart/gtp-shared-components';

const [selectedSegment, setSelectedSegment] = React.useState(0);

<Segmented
  size="small"
  selectedIndex={selectedSegment}
  onChange={(index) => setSelectedSegment(index)}>
  <Segment>First</Segment>
  <Segment>Second</Segment>
  <Segment>Third</Segment>
</Segmented>;
```

### Migration using Codemods

As we mentioned in the intro, we are providing automation scripts to assist you with the migration from `legacy` to `next`.
We are using `jscodeshift` from Facebook. Here are the details:

NOTE: Install JSCodeshift globally before running codemods

```bash
  npm install -g jscodeshift
```

We have added a script called `runCodemods` with JSCodeshift that helps automating the breaking changes above on your application when upgrading our library.

#### Usage

```bash
npx runCodemods <transform>         --> runs on the Project root folder.
npx runCodemods <transform> <path>  --> runs on a specific folder or file.
```

where:

- transform - name of transform, see available transforms below.
- path - files or directory to transform if path is empty it will run on project root folder

This will start an interactive wizard, and then run the specified transform.
Once you install the library in your project, all the codemods transform scripts are going to be placed under `node_modules/.bin` and can be run via `npx`.

>

#### Included Transforms

##### updateImports

> Change to import from root instead of `dist`. Please see `Example1` above for a sample of what will change.
>
> ```bash
> npx runCodemods updateImports <path>
> ```

##### updateJestConfig

> Add `gtp-shared-icons` to the `transformIgnorePatterns` jest config prop.
> It checks the jest.config.js/mjs/cjs/ts or package.json to see if transformIgnorePatterns prop has `@walmart/gtp-shared-components` and `@walmart/gtp-shared-icons` in the list, if not then it will add them.
>
> ```bash
> npx runCodemods updateJestConfig <path>
> ```
>
> **Before: jest.config/package.json**
>
> ```js static noeditor
> transformIgnorePatterns: ['<rootDir>/node_modules/(?!(react-native)'];
> ```
>
> **After: jest.config/package.json**
>
> ```js static noeditor
> transformIgnorePatterns: [
>   '<rootDir>/node_modules/(?!(react-native|@walmart/gtp-shared-components|@walmart/gtp-shared-icons)',
> ];
> ```

##### updateStyle

> Change `style` with `UNSAFE_style`.
> Example:
>
> **before**
>
> ```
> <Body style={styles.normal}>something</Body>
> ```
>
> **after**
>
> ```
> <Body UNSAFE_style={styles.normal}>something</Body>
> ```
>
> ```bash
> npx runCodemods updateStyle <path>
> ```

#### Example app

- we have done a major re-vamp of the embedded example app. Things are better separated, easier to visualize. Also added many component variant showcases.
- the app has been renamed to `LDRNExample`
- we added a separate section on the home page which is a collection of `Recipes`. Here we are showcasing more advanced examples of components usage.

#### Picker dependencies

- If your app is using `@walmart/gtp-shared-components@1.7.0` and above (that ofc includes `2.0.*`), you need to install the following dependencies in your app :

  ```json static noeditor
  yarn add @react-native-picker/picker
  yarn add @react-native-community/datetimepicker
  ```

NOTE regarding the date picker component: the `next` version is still using the `legacy` date pickers which have platform specific look and feel (modal for Android, bottom sheet wheel(s)) for iOS. We are in the process of replacing this with the new DatePicker, aligned with LD3 which is going to be platform agnostic i.e. it will have the same look and feel on both iOS and Android. The design specs were not ready at the time of this release, so we had to defer this one for a future release.

### Added

#### Fonts

- We have added a script called `installFonts` which automates the installation of fonts in the native scaffolds (iOS, Android). This script can be invoked via npx like this:

  ```shell static noeditor
  npx installFonts
  ```

  The script installs the fonts found under
  `node_modules/@walmart/gtp-shared-components/assets/fonts`
  to:

  - Android
    - android/app/src/main/assets/fonts
    - android/link-assets-manifest.json
  - iOS
    - ios/[your_project]/Info.plist
    - ios/link-assets-manifest.json
    - ios/[your_project].xcodeproj/project.pbxproj
    - add group 'Resources' in the Xcode project

  The script looks for a file called `react-native.config.js` with the following sections:

  ```js static noeditor
  module.exports = {
    project: {
      ios: {},
      android: {},
    },
    assets: ['.node_modules/@walmart/gtp-shared-components/assets/fonts'],
  };
  ```

  If this file doesn't exist, it creates it for you.
  NOTE: installFonts _does not_ commit any changes, it's up to you to verify the changes and commit.

#### Icons

- All icons have been extracted into a separate repo, `gtp-shared-icons`. However, this change is transparent to you, the icons imports remain the same as before.

  ```js static noeditor
  import {Icons} from '@walmart/gtp-shared-components';

  <Icons.CloseIcon />;
  ```

## Release 2.0.0 tickets:

- [CEEMP-2777](https://jira.walmart.com/browse/CEEMP-2777) Feature Request - ability to pass custom content to BottomSheet
- [CEEMP-2767](https://jira.walmart.com/browse/CEEMP-2767) Feature Request - Select component where options should render top of the screen
- [CEEMP-2810](https://jira.walmart.com/browse/CEEMP-2810) Feature Request - TextField TextArea display error only on submit
- [CEEMP-2829](https://jira.walmart.com/browse/CEEMP-2813) Feature Request - Callout customize Close button text
- [CEEMP-2809](https://jira.walmart.com/browse/CEEMP-2809) Feature Request - Heading font size
- [CEEMP-2813](https://jira.walmart.com/browse/CEEMP-2813) Feature Request - TextField recipe for validate on submit, hide error message when typing
- [CEEMP-2761](https://jira.walmart.com/browse/CEEMP-2761) Bug Report: Content of the ListItem doesn't align correctly with the List.
- [CEEMP-2790](https://jira.walmart.com/browse/CEEMP-2790) Bug Report - Callout alignment with custom styling of trigger Link
- [CEEMP-2794](https://jira.walmart.com/browse/CEEMP-2794) Bug Report - BottomSheet action spacing
- [CEEMP-2808](https://jira.walmart.com/browse/CEEMP-2808) Bug Report - ProgressIndicator typing issue fix
- [CEEMP-2764](https://jira.walmart.com/browse/CEEMP-2764) Bug Report - List Scroll Issue
- [CEEMP-2811](https://jira.walmart.com/browse/CEEMP-2811) Bug Report - TabNavigation responsiveness
- [CEEMP-2803](https://jira.walmart.com/browse/CEEMP-2803) Export TS types from all components
- [CEEMP-2802](https://jira.walmart.com/browse/CEEMP-2802) Align + refactor: gap visible in focus state
- [CEEMP-2793](https://jira.walmart.com/browse/CEEMP-2793) Align + refactor: Omit style from all props
- [CEEMP-2805](https://jira.walmart.com/browse/CEEMP-2805) Implement codemods for adding gtp-shared-icons into the jest.config.js
- [CEEMP-2821](https://jira.walmart.com/browse/CEEMP-2821) Implement codemods for replacing style with UNSAFE_style
- [CEEMP-2827](https://jira.walmart.com/browse/CEEMP-2827) Update CHANGELOG for the 2.0 GA release

## Release 2.0.0-rc.2

- [CEEMP-2786](https://jira.walmart.com/browse/CEEMP-2786) Feature Request - Back button on BottomSheet
- [CEEMP-2787](https://jira.walmart.com/browse/CEEMP-2787) Bug Report - Bogle font not used Android RN 0.70

## Release 2.0.0-rc.1

- [CEEMP-2772](https://jira.walmart.com/browse/CEEMP-2772) Feature Request - useSnackbar customization
- [CEEMP-2778](https://jira.walmart.com/browse/CEEMP-2778) Feature Request - Select with BottomSheet - add Cancel button from multi
- [CEEMP-2785](https://jira.walmart.com/browse/CEEMP-2785) update library with the latest gtp-shared-icons, 1.0.5 (aligned with LD 0.4.38)
- [CEEMP-2765](https://jira.walmart.com/browse/CEEMP-2765) Bug Report : Extra space at bottom of BottomSheet
- [CEEMP-2769](https://jira.walmart.com/browse/CEEMP-2769) Bug Report: Card background shadow
- [CEEMP-2768](https://jira.walmart.com/browse/CEEMP-2768) Bug Report: Chip prop is set to true or false it will still toggle
- [CEEMP-2268](https://jira.walmart.com/browse/CEEMP-2268) Bug Report: BottomSheet - Keyboard overlays InputText
- [CEEMP-2779](https://jira.walmart.com/browse/CEEMP-2779) Bug Report - Select with multi-choice - Android does not render properly
- [CEEMP-2780](https://jira.walmart.com/browse/CEEMP-2780) Bug Report - BottomSheet fullWidth not working on tablets

## Release 2.0.0-beta.11

- [CEEMP-2756](https://jira.walmart.com/browse/CEEMP-2756) Feature Request - open BottomSheet with list of options instead of default dropdown
- [CEEMP-2748](https://jira.walmart.com/browse/CEEMP-2748) Bug Report - Select component onPress not working
- [CEEMP-2760](https://jira.walmart.com/browse/CEEMP-2760) Bug Report - Checkbox LD style
- [CEEMP-2761](https://jira.walmart.com/browse/CEEMP-2761) Bug Report : Bug Report: Content of the ListItem doesn't align correctly with the List.
- [CEEMP-2763](https://jira.walmart.com/browse/CEEMP-2763) Bug Report : Buttons were resizing
- [CEEMP-2764](https://jira.walmart.com/browse/CEEMP-2764) Bug Report: List Scroll Issue
- [CEEMP-2770](https://jira.walmart.com/browse/CEEMP-2770) Bug Report: Alerts variant LD3 style

## Release 2.0.0-beta.10

- [CEEMP-2727](https://jira.walmart.com/browse/CEEMP-2727) Organizing Imports with ESLint plugin
- [CEEMP-2736](https://jira.walmart.com/browse/CEEMP-2736) Bug Report - Chip Component mismatch
- [CEEMP-2743](https://jira.walmart.com/browse/CEEMP-2743) Bug Report - icon color change
- [CEEMP-2747](https://jira.walmart.com/browse/CEEMP-2747) Bug Report - Bottom sheet font styling
- [CEEMP-2749](https://jira.walmart.com/browse/CEEMP-2749) Bug Report - BottomSheet button goes offscreen
- [CEEMP-2750](https://jira.walmart.com/browse/CEEMP-2750) Bug Report : Radio button color does not match LD3
- [CEEMP-2759](https://jira.walmart.com/browse/CEEMP-2759) Bug Report: TabNavigation borderless style issue

## Release 2.0.0-beta.9

- [CEEMP-2639](https://jira.walmart.com/browse/CEEMP-2639) align + refactor: DataTable (new)
- [CEEMP-2708](https://jira.walmart.com/browse/CEEMP-2708) align + refactor: implement codemods for changing imports

## Release 2.0.0-beta.8

- [CEEMP-2530](https://jira.walmart.com/browse/CEEMP-2530) align + refactor Callout (currently Tooltip)
- [CEEMP-2538](https://jira.walmart.com/browse/CEEMP-2538) align + refactor Popover (new component)
- [CEEMP-2690](https://jira.walmart.com/browse/CEEMP-2690) align + refactor Menu (new)
- [CEEMP-2695](https://jira.walmart.com/browse/CEEMP-2695) align + refactor: fix Progress Tracker Label overflow issue fix
- [CEEMP-2699](https://jira.walmart.com/browse/CEEMP-2699) align + refactor BottomSheet unit tests
- [CEEMP-2703](https://jira.walmart.com/browse/CEEMP-2703) align + refactor: accessibility: refactor testID
- [CEEMP-2704](https://jira.walmart.com/browse/CEEMP-2704) TabNavigator styleguide update
- [CEEMP-2705](https://jira.walmart.com/browse/CEEMP-2705) align + refactor: add helper script findToken
- [CEEMP-2710](https://jira.walmart.com/browse/CEEMP-2710) Upgrade Components to support LD Tokens 0.60.2
- [CEEMP-2713](https://jira.walmart.com/browse/CEEMP-2713) align + refactor: add new size options to icons
- [CEEMP-2714](https://jira.walmart.com/browse/CEEMP-2714) Bug Report - styling prop for older react-native versions
- [CEEMP-2718](https://jira.walmart.com/browse/CEEMP-2718) align + refactor: add diffTokens script
- [CEEMP-2719](https://jira.walmart.com/browse/CEEMP-2719) align + refactor: upgrade tokens to 0.61.0
- [CEEMP-2721](https://jira.walmart.com/browse/CEEMP-2721) align + refactor: upgrade icons to 1.0.4

## Release 2.0.0-beta.7

- [CEEMP-2692](https://jira.walmart.com/browse/CEEMP-2692) Alert & Banner components should wrap longer children content
- [CEEMP-2694](https://jira.walmart.com/browse/CEEMP-2694) re-branding example app and docs to LivingDesign
- [CEEMP-2543](https://jira.walmart.com/browse/CEEMP-2543) align + refactor Segment, Segmented
- [CEEMP-2544](https://jira.walmart.com/browse/CEEMP-2544) new component Select (former Dropdown)
- [CEEMP-2528](https://jira.walmart.com/browse/CEEMP-2528) align + refactor BottomSheet
- [CEEMP-2698](https://jira.walmart.com/browse/CEEMP-2698) add missing Bogle fonts to Android native in example app
- [CEEMP-2689](https://jira.walmart.com/browse/CEEMP-2689) fix documentation for Props and Methods for all components
- [CEEMP-2700](https://jira.walmart.com/browse/CEEMP-2700) change ChipGroup to take Chip's as children instead of array
- [CEEMP-2701](https://jira.walmart.com/browse/CEEMP-2701) add accessibilityRole to all components
- [CEEMP-2702](https://jira.walmart.com/browse/CEEMP-2702) add accessibilityState to all components

## Release 2.0.0-beta.6

- [CEEMP-2533](https://jira.walmart.com/browse/CEEMP-2533) align + refactor FormGroup
- [CEEMP-2545](https://jira.walmart.com/browse/CEEMP-2545) align + refactor Skeleton
- [CEEMP-2550](https://jira.walmart.com/browse/CEEMP-2550) align + refactor TabNavigation
- [CEEMP-2551](https://jira.walmart.com/browse/CEEMP-2551) align + refactor TextArea
- [CEEMP-2553](https://jira.walmart.com/browse/CEEMP-2553) align + refactor Variants (non LD3)
- [CEEMP-2637](https://jira.walmart.com/browse/CEEMP-2637) align + refactor TextField: unit tests
- [CEEMP-2666](https://jira.walmart.com/browse/CEEMP-2666) Bug Report - Switch component

## Release 2.0.0-beta.5

- [CEEMP-2552](https://jira.walmart.com/browse/CEEMP-2552) align + refactor TextField
- [CEEMP-2660](https://jira.walmart.com/browse/CEEMP-2660) bk compatibility: BottomSheetsScreen Carousel
- [CEEMP-2658](https://jira.walmart.com/browse/CEEMP-2658) align + refactor: bk compatibility: invalid color for Spinner
- [CEEMP-2627](https://jira.walmart.com/browse/CEEMP-2627) align + refactor: change renderLeading renderTrailing
- [CEEMP-2540](https://jira.walmart.com/browse/CEEMP-2540) align + refactor ProgressTracker
- [CEEMP-2675](https://jira.walmart.com/browse/CEEMP-2675) TextField onChangeText type mismatch
- [CEEMP-2462](https://jira.walmart.com/browse/CEEMP-2462) align + refactor: Error Message component

## Release 2.0.0-beta.4

- [CEEMP-2654](https://jira.walmart.com/browse/CEEMP-2654) Support for legacy Snackbar
- [CEEMP-2664](https://jira.walmart.com/browse/CEEMP-2664) remove invalid style prop whiteSpace
- [CEEMP-2650](https://jira.walmart.com/browse/CEEMP-2650) extract HomeScreenHeader in example
- [CEEMP-2654](https://jira.walmart.com/browse/CEEMP-2654) Backwards compatibility for Snackbar
- [CEEMP-2659](https://jira.walmart.com/browse/CEEMP-2659) IconButton backwards compatibility issue
- [CEEMP-2653](https://jira.walmart.com/browse/CEEMP-2653) List backwards compatibility support
- [CEEMP-2523](https://jira.walmart.com/browse/CEEMP-2523) Add Rating Component
- [CEEMP-2656](https://jira.walmart.com/browse/CEEMP-2656) BottomSheet backwards compatibility issue
- [CEEMP-2668](https://jira.walmart.com/browse/CEEMP-2656) segregate next vs legacy releases in npme

## Release 2.0.0-beta.3

- [CEEMP-2662](https://jira.walmart.com/browse/CEEMP-2662) remove pointerEvents in DropdownPicker
- [CEEMP-2638](https://jira.walmart.com/browse/CEEMP-2638) Picker theme added in form

## Release 2.0.0-beta.2

- [CEEMP-2536](https://jira.walmart.com/browse/CEEMP-2536) add new component Modal
- [CEEMP-2564](https://jira.walmart.com/browse/CEEMP-2564) add new component Metric
- [CEEMP-2641](https://jira.walmart.com/browse/CEEMP-2641) add unit tests for Modal
- [CEEMP-2642](https://jira.walmart.com/browse/CEEMP-2642) add unit tests for useSnackbar
- [CEEMP-2643](https://jira.walmart.com/browse/CEEMP-2643) provide legacy docs in README
- [CEEMP-2646](https://jira.walmart.com/browse/CEEMP-2646) fix styling bug in DropdownPicker
- [CEEMP-2537](https://jira.walmart.com/browse/CEEMP-2537) add new component Nudge
- [CEEMP-2644](https://jira.walmart.com/browse/CEEMP-2644) hide snackbar after action button press
- [CEEMP-2647](https://jira.walmart.com/browse/CEEMP-2647) add new component List
- [CEEMP-2652](https://jira.walmart.com/browse/CEEMP-2652) fix mockdate bug

---

## Releases prior to 2.0

## Release 1.8.18

### Fixed

- [CEEMP-2787](https://jira.walmart.com/browse/CEEMP-2787) Bug Report - Bogle font not used Android
- (chore) fix Android build in example app

## Release 1.8.17

### Fixed

- [CEEMP-2745](https://jira.walmart.com/browse/CEEMP-2745) Feature Request - need Secondary button to accept ref

## Release 1.8.16

### Fixed

- [CEEMP-2730](https://jira.walmart.com/browse/CEEMP-2730) Bug Report - Button loading activity indicator offcenter
- [CEEMP-2728](https://jira.walmart.com/browse/CEEMP-2728) Feature Request - move accessibilityState above rootProps

## Release 1.8.15

### Fixed

- [CEEMP-2714](https://jira.walmart.com/browse/CEEMP-2714) Bug Report - styling prop for older react-native versions

---

## Release 1.8.14

### Fixed

- [CEEMP-2682](https://jira.walmart.com/browse/CEEMP-2682) Checkbox styling Android
- [CEEMP-2687](https://jira.walmart.com/browse/CEEMP-2687) ProgressTracker label overlap
- [CEEMP-2691](https://jira.walmart.com/browse/CEEMP-2691) Badge number positioning

---

## Release 1.8.13

### Fixed

- [CEEMP-2680](https://jira.walmart.com/browse/CEEMP-2680) Overlay Component Darken Issue fix
- [CEEMP-2678](https://jira.walmart.com/browse/CEEMP-2678) CountBadge font weight Android Issue fix

---

## Release 1.8.12

### Fixed

- [CEEMP-2669](https://jira.walmart.com/browse/CEEMP-2669) BottomSheet keyboard issue fix
- [CEEMP-2655](https://jira.walmart.com/browse/CEEMP-2655) Backward compatibility support FormsScreen RadioItemGroup

---

## Release 1.8.11

### Fixed

- [CEEMP-2664](https://jira.walmart.com/browse/CEEMP-2664) remove invalid style prop whiteSpace
- [CEEMP-2657](https://jira.walmart.com/browse/CEEMP-2657) chips crash fix in legacy example

---

## Release 1.8.10

### Fixed

- [CEEMP-2662](https://jira.walmart.com/browse/CEEMP-2662) remove pointerEvents in DropdownPicker

### Added

- [CEEMP-2638](https://jira.walmart.com/browse/CEEMP-2638) Picker theme added in form

---

## Release 1.8.9

### Fixed

- [CEEMP-2646](https://jira.walmart.com/browse/CEEMP-2646) fix styling bug in DropdownPicker

### Added

- [CEEMP-2643](https://jira.walmart.com/browse/CEEMP-2643) Provide legacy docs in the README

---

## Release 1.8.8

### Fixed

- removed unused package react-keyed-flatten-children

---

## Release 1.8.7

### Added

[CEEMP-2623](https://jira.walmart.com/browse/CEEMP-2623) BottomSheet add logic for Android back button
[CEEMP-2569](https://jira.walmart.com/browse/CEEMP-2569) Legacy Chips support Custom Icons

---

## Release 1.8.6

### Fixed

[CEEMP-2571](https://jira.walmart.com/browse/CEEMP-2571) Fix for Boggle font family in Themed Buttons on Android

---

## Release 1.8.5

### Added

[CEEMP-2576](https://jira.walmart.com/browse/CEEMP-2576) add prop onResize to BottomSheet to expose height of component

```js static noeditor
/**
   * Resize event handler.
   * this will be called with `height` as argument
   * so it can be used to get the current height of
   * the BottomSheet
   */
  onResize?: (height?: number | undefined) => void;
```

---

## Release 1.8.4

### Added

- [CEEMP-2559](https://jira.walmart.com/browse/CEEMP-2559) added example component ListWithCheckbox (for PS-Learning team)

---

## Release 1.8.3

### Fixed

- [CEEMP-2490](https://jira.walmart.com/browse/CEEMP-2490) - Bug Report - Android talk back issue DropDown - done

- [CEEMP-2396](https://jira.walmart.com/browse/CEEMP-2396) - Android: Dropdown: TalkBack: announced as disabled

---

## Release 1.8.2

### Added

- [CEEMP-2510](https://jira.walmart.com/browse/CEEMP-2510) - add optional prop keyboardShouldPersistProps to BottomSheet (thanks Rahil Manzar!)

- [CEEMP-2504](https://jira.walmart.com/browse/CEEMP-2504) - add more logic to .looper.yml

---

## Release 1.8.1

### Added

- [CEEMP-2412](https://jira.walmart.com/browse/CEEMP-2412) - add 'isFullWidth' prop for button components + mark block prop as deprecated

- [CEEMP-2503](https://jira.walmart.com/browse/CEEMP-2503) - add behavior to CardOverlay- tap outside to dismiss

- [CEEMP-2504](https://jira.walmart.com/browse/CEEMP-2504) - add looper flow to auto-generate Styleguidist documentation after publishing

---

## Release 1.8.0

### Added

- CEEMP-2499 - added new prop closeButton (icon button (close (X))) to Snackbar

- CEEMP-2500 - added support for using React Native Debugger which provides superior developer experience compared to devtools.

### Changed

- CEEMP-2478 - complete UI/Ux revamp of the example embedded app for cleaner, better visualization of components

### Fixed

- CEEMP-2497 - corrected language in peerDependencies section in the README file
- various internal bug fixes and documentation updates

---

## Release 1.7.3

### Added

- [CEEMP-2494](https://jira.walmart.com/browse/CEEMP-2494) added custom CardOverlay example

---

## Release 1.7.2

### Added

- added dedicated screen for BottomSheet examples in the example app

### Fixed

- [CEEMP-2470](https://jira.walmart.com/browse/CEEMP-2596) - fix Props & Methods in the docs

- [CEEMP-2493](https://jira.walmart.com/browse/CEEMP-2596) - fix TextField link in the docs

- [CEEMP-2440](https://jira.walmart.com/browse/CEEMP-2596) - fix BottomSheet lock UI bug

---

## Release 1.7.1

### Fixed

- corrected picker module reference from @react-native-community/picker to @react-native-picker/picker

---

## Release 1.7.0

### Breaking

- starting with this release, you need to install the following dependencies in your app :

  ```json static noeditor
  yarn add @react-native-picker/picker
  yarn add @react-native-community/datetimepicker
  ```

### Added

- added Storybook stories for part of the components
- added .insights.yml file

### Changed

- started the process of eliminating imports from dist
- moved @react-native-community/datetimepicker and @react-native-community/picker to peerDependencies. Please read the new Peer Dependencies paragraph in the README.md for more details.

### Fixed

- fixed FilledFlag bug
- fixed Styleguidist documentation

---

## Release 1.6.0

### Added

- added living design tokens to drive the visual design of the Primary, Secondary, Tertiary, Destructive buttons components
- added new Tertiary button
- added size prop for Primary, Secondary, Tertiary, Destructive buttons. The default size of all buttons is ‘small’.‘small’ prop is not removed but default size of these buttons will be small instead of medium.
  #93

### Changed

- updated storybook version to 6.4.17 #104

### Fixed

- While running tests you could run into an open issue where livingdesign tokens are not being transformed by Jest

  Sample Error Message

  ```js noeditor static
  export const componentButtonContainerAlignHorizontal = "center";
  ^^^^^^
  SyntaxError: Unexpected token export
  ```

  Recommended Solution

  'whitelist' livingdesign token node_modules in package.json jest config like this

  ```json static noeditor
  "jest": {
      "transformIgnorePatterns": [
        "node_modules/(?!@ngrx|(?!livingdesign))"
      ]
    }
  ```

  GTP SC and Living Design Teams are working towards a permanent solution in a future release.

---

## Release 1.5.1

### Changed

- re-generated icons from Living Design
