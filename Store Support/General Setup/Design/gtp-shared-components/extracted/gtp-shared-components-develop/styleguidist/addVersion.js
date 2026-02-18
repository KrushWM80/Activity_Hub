/* eslint-env browser */
// Add the package.json version to the sidebar
import {version} from '../package.json';

const duration = 125;
const selector = '[class*="sidebar"] h1';
let tries = 20;
let timer;

const addVersion = () => {
  tries -= 1;

  if (!tries) {
    clearTimeout(timer);
  } else if (!document.querySelector(selector)) {
    timer = setTimeout(addVersion, duration);
  } else {
    document.querySelector(
      selector,
    ).innerHTML += ` <small style="opacity: 0.4">v${version}</small>`;
  }
};

addVersion();
