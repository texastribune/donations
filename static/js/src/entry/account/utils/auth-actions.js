import auth from './auth';
import {
  AUTH_PORTAL_CLIENT_ID,
  AUTH_PORTAL_LOGOUT_COMPLETE_URL,
  NON_STAFF_CONNECTION,
} from '../constants';
import {
  setPostLogOutRedirect,
  getPostLogOutRedirect,
  clearPostLogOutRedirect,
  setPostLogInRedirect,
  getPostLogInRedirect,
  clearPostLogInRedirect,
} from './storage';

export const logIn = () => {
  setPostLogInRedirect();
  auth.authorize({ initial_screen: 'login' });
};

export const logOut = () => {
  setPostLogOutRedirect();
  auth.logout({
    clientID: AUTH_PORTAL_CLIENT_ID,
    returnTo: AUTH_PORTAL_LOGOUT_COMPLETE_URL,
  });
};

export const register = () => {
  auth.authorize({ initial_screen: 'signUp' });
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};

export const redirectAfterLogIn = () => {
  setTimeout(() => {
    const url = getPostLogInRedirect();
    clearPostLogInRedirect();
    window.location.href = url || '/account/';
  }, 1800);
};

export const redirectAfterLogOut = () => {
  setTimeout(() => {
    const url = getPostLogOutRedirect();
    clearPostLogOutRedirect();
    window.location.href = url || '/donate';
  }, 1800);
};
