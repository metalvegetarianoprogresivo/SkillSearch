/*
  This module sets the data to use on when the server is started. Each option is given by the TEST_DATA environmental variable.
  There are two options:
    - CLEAN: Sets a clean dataset.
    - KIMBLE: Sets a dataset based on a kimble dump.
*/

var consultantInfo
var consultantAssignments

switch(process.env.TEST_DATA){
  case "CLEAN":
    consultantInfo = require('./db_consultant_info_clean_data.json')
    consultantAssignments = require('./db_consultant_assignments_clean_data.json')
  break;
  case "KIMBLE":
    consultantInfo = require('./db_consultant_info_kimble_dump.json')
    consultantAssignments = require('./db_consultant_assignments_kimble_dump.json')
  break;
}

module.exports = function() {
  return {
    consultantInfo: consultantInfo,
    consultantAssignments: consultantAssignments
  }
}
