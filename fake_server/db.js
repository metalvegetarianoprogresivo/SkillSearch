/*
  This module sets the data to use when the server is started.
  The value is specified on the test_data attribute of the data_config.json file.
  There are two options:
    - EMPTY: To set am empty dataset.
    - KIMBLE: Sets a dataset based on a kimble dump.
*/

const dataConfig = require('./data_config.json');

module.exports = function() {

  return {
    serverOAuth: require(dataConfig.server_oauth),
    consultantInfo: dataConfig.test_data === 'KIMBLE' ? require(dataConfig.kimble.consultant_info) : require(dataConfig.empty.consultant_info),
    consultantAssignments: dataConfig.test_data === 'KIMBLE' ? require(dataConfig.kimble.consultant_assignments) : require(dataConfig.empty.consultant_assignments)
  }
}
