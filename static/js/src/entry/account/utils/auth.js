import { WebAuth } from 'auth0-js';

import {
  AUTH_DOMAIN,
  AUTH_PORTAL_AUDIENCE,
  AUTH_PORTAL_CLIENT_ID,
  AUTH_PORTAL_LOGIN_COMPLETE_URL,
} from '../constants';

const auth = new WebAuth({
  domain: AUTH_DOMAIN,
  audience: AUTH_PORTAL_AUDIENCE,
  redirectUri: AUTH_PORTAL_LOGIN_COMPLETE_URL,
  clientID: AUTH_PORTAL_CLIENT_ID,
  responseType: 'code',
  scope: 'openid email profile',
});

export default auth;
