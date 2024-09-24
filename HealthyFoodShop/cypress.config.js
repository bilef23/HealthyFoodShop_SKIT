module.exports = {
  e2e: {
    setupNodeEvents(on, config) {
     require('@cypress/code-coverage/task')(on, config)

      return config
    },
    baseUrl: 'http://localhost:8000',
    defaultCommandTimeout: 10000,
  },
};
