/* eslint-env browser */
// Add the package.json version to the sidebar
import {version} from '../package.json';

const duration = 125;
const selector = '[class*="sidebar"] h1';
let tries = 20;
let timer;

const maybeAdd = () => {
  tries -= 1;

  if (!tries) {
    clearTimeout(timer);
  } else if (!document.querySelector(selector)) {
    timer = setTimeout(maybeAdd, duration);
  } else {
    document.querySelector(
      selector,
    ).innerHTML += ` <small style="opacity: 0.4">v${version}</small>`;
  }
};

maybeAdd();
