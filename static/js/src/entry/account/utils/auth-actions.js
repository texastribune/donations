import auth from './auth';
import {
  AUTH_PORTAL_CLIENT_ID,
  AUTH_PORTAL_LOGOUT_COMPLETE_URL,
  AUTH_PORTAL_LOGIN_COMPLETE_URL,
  NON_STAFF_CONNECTION,
} from '../constants';

export const logIn = (next = '/account/') => {
  auth.authorize({
    initial_screen: 'login',
    redirectUri: `${AUTH_PORTAL_LOGIN_COMPLETE_URL}?next=${next}`,
  });
};

export const logOut = (next = '/donate') => {
  auth.logout({
    clientID: AUTH_PORTAL_CLIENT_ID,
    returnTo: `${AUTH_PORTAL_LOGOUT_COMPLETE_URL}?next=${next}`,
  });
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};

export const redirect = next => {
  setTimeout(() => {
    window.location.href = next;
  }, 1800);
};
