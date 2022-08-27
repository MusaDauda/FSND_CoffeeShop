
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-bge3486a.us', // the auth0 domain prefix
    audience: 'mycoffee', // the audience set for the auth0 app
    clientId: 'szyKQHu5SYoEd4nshtg0XN2gR5GxHxbW', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
