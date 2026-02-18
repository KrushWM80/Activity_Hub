---
sh: "gh release create <%= `v${new_version}` %> -t <%= `v${new_version}` %> -d -n '\n ## Whats Changed \n\n### Enhancements : \n\n <%= change_log %>  <%= previous_version ? `\n \n ** Full Changelog **: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons/compare/v${previous_version}...v${new_version}` : `\n` %> '"
---
