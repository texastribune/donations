import { WebAuth } from 'auth0-js';

import {
  AUTH_DOMAIN,
  AUTH_CLIENT_ID,
  AUTH_LOGIN_COMPLETE_URL,
} from '../constants';

const auth = new WebAuth({
  domain: AUTH_DOMAIN,
  redirectUri: AUTH_LOGIN_COMPLETE_URL,
  clientID: AUTH_CLIENT_ID,
  responseType: 'code',
  scope: 'openid profile email',
});

export default auth;
