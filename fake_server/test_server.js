const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router(require('./db.js')()) // Use the db
const middlewares = jsonServer.defaults()

const PORT = 3010;

// Custom routes constants
const consultantInfoNameLinksRoute = '/services/data/v24.0/query?q=SELECT%20Name,KimbleOne__Resource__c.Resource_Bio__r.Bio_Url__c%20FROM%20KimbleOne__Resource__c%20WHERE%20KimbleOne__ResourceType__c%20=%20%27a7J0c000002VD4LEAW%27%20AND%20KimbleOne__Grade__c%20%21=%20%27a5G0c000000g2IXEAY%27%20AND%20KimbleOne__StartDate__c%20%3C=%20TODAY%20AND%20KimbleOne__EndDate__c%20=%20Null';
const consultantInfoLocationRoute = '/services/data/v24.0/query\\?q=%20SELECT%20KimbleOne__Resource__c.KimbleOne__BusinessUnit__r.Name%20FROM%20KimbleOne__Resource__c%20WHERE%20name%20=%20%27:name%27';
const consultantInfoTitleRoute = '/services/data/v24.0/query\\?q=%20SELECT%20KimbleOne__Resource__c.KimbleOne__Grade__r.Name%20FROM%20KimbleOne__Resource__c%20WHERE%20name%20=%20%27:name%27';
const consultantInfoEmailRoute = '/services/data/v24.0/query\\?q=%20SELECT%20KimbleOne__Resource__c.KimbleOne__User__r.Email%20FROM%20KimbleOne__Resource__c%20WHERE%20name%20=%20%27:name%27';
const consultantAssignmentsRoute = '/services/data/v24.0/query\\?q=%20SELECT%20name,%20KimbleOne__Resource__r.Name,%20KimbleOne__DeliveryGroup__r.KimbleOne__Account__r.Name,%20KimbleOne__StartDate__c,%20KimbleOne__ForecastP1EndDate__c,%20KimbleOne__ForecastP2EndDate__c,%20KimbleOne__ForecastP3EndDate__c,%20KimbleOne__UtilisationPercentage__c%20FROM%20KimbleOne__ActivityAssignment__c%20WHERE%20KimbleOne__DeliveryGroup__c%20%21=%20NULL%20AND%20KimbleOne__Resource__r.Name%20=%20%27:name%27';

// Remove the request.query value when the first route is used so the server does not try to query.
// This is needed since on the first route was not possible to escape the ? symbol
server.use((req, res, next) => {
  if(req.originalUrl == consultantInfoNameLinksRoute){
    req.query = {}
  }
  next()
})

server.use(middlewares)

// Configure the custom routes
server.use(
  jsonServer.rewriter({
    [consultantInfoNameLinksRoute] : '/consultantInfo',
    [consultantInfoLocationRoute]: '/consultantInfo?Name=:name',
    [consultantInfoTitleRoute]: '/consultantInfo?Name=:name',
    [consultantInfoEmailRoute]: '/consultantInfo?Name=:name',
    [consultantAssignmentsRoute]: '/consultantAssignments/?KimbleOne__Resource__r.Name=:name'
  })
)

server.use(router)


server.listen(PORT, () => {
  console.log('JSON Server is running on port: ' + PORT)
})


// Funtion that customizes the output response
router.render = (req, res) => {

  // Custom error message in case one route is not found
  if (res.statusCode == 404) {
    res.status(404).jsonp({
      error: "Resource not found"
    })
  } else {
    // Custom output so the response match with the expected response by the application
    res.jsonp({
      totalSize: 401,
      done: true,
      records: res.locals.data
    })
  }
}
