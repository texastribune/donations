import auth from './auth';

import {
  AUTH_PORTAL_CLIENT_ID,
  AUTH_PORTAL_LOGOUT_COMPLETE_URL,
  AUTH_PORTAL_LOGIN_COMPLETE_URL,
  NON_STAFF_CONNECTION,
} from '../constants';

const createRedirectQueryParams = ({ redirectName, redirectQueryParams }) => {
  let queryParams = `redirectName=${redirectName}`;

  if (redirectQueryParams) {
    queryParams += `&redirectQueryParams=${encodeURIComponent(
      JSON.stringify(redirectQueryParams)
    )}`;
  }

  return queryParams;
};

export const logIn = (info = {}) => {
  const queryParams = createRedirectQueryParams({
    redirectName: 'accountOverview',
    ...info,
  });

  auth.authorize({
    initial_screen: 'login',
    redirectUri: `${AUTH_PORTAL_LOGIN_COMPLETE_URL}?${queryParams}`,
  });
};

export const logOut = (info = {}) => {
  const queryParams = createRedirectQueryParams({
    redirectName: 'donate',
    ...info,
  });

  auth.logout({
    clientID: AUTH_PORTAL_CLIENT_ID,
    returnTo: `${AUTH_PORTAL_LOGOUT_COMPLETE_URL}?${queryParams}`,
  });
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};
