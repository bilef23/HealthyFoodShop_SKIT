const codeCoverage = require('@cypress/code-coverage/task');

module.exports = (on) => {
  codeCoverage(on);
};
