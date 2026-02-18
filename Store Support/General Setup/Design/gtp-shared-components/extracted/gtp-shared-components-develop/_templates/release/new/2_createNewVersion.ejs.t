---
sh: "npm version <%= (`${locals.releaseType}` === 'prepatch' || `${locals.releaseType}` === 'preminor' || `${locals.releaseType}` === 'premajor' || `${locals.releaseType}` === 'prerelease') ? `${locals.releaseType} --preid rc` : `${locals.releaseType}` %>"
---
