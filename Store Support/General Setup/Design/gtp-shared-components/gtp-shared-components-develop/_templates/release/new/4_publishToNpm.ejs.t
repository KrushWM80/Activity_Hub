---
sh: "npm publish <%= (`${locals.releaseType}` === 'prepatch' || `${locals.releaseType}` === 'preminor' || `${locals.releaseType}` === 'premajor' || `${locals.releaseType}` === 'prerelease') ? `--tag prerelease-rc` : (`${locals.new_version}`.startsWith('1.'))? `--tag legacy` : '' %>"
---
