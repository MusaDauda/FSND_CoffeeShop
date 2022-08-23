
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-bge3486a.us', // the auth0 domain prefix
    audience: 'coffeestore', // the audience set for the auth0 app
    clientId: 'r4n8DInACbMaeJSDuFRD32duUuXOtsZk', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
