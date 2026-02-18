// see types of prompts:
// https://github.com/enquirer/enquirer/tree/master/examples
//
module.exports = [
  {
    type: 'input',
    name: 'new_version',
    message: 'enter new version number?',
  },
  {
    type: 'input',
    name: 'previous_version',
    message: 'enter Previous version number?',
  },
  {
    type: 'input',
    name: 'change_log',
    message: 'whats changed?',
  },
];
