import auth from './auth';
import {
  LOGGED_IN_FLAG_KEY,
  AUTH_CLIENT_ID,
  AUTH_LOGOUT_COMPLETE_URL,
  LOGIN_REDIRECT_KEY,
  LOGOUT_REDIRECT_KEY,
  NON_STAFF_CONNECTION,
} from '../constants';

export const clearFlag = () => {
  localStorage.removeItem(LOGGED_IN_FLAG_KEY);
};

export const setFlag = () => {
  localStorage.setItem(LOGGED_IN_FLAG_KEY, true);
};

export const logIn = () => {
  localStorage.setItem(LOGIN_REDIRECT_KEY, window.location.href);
  auth.authorize({ initial_screen: 'login' });
};

export const logOut = () => {
  localStorage.setItem(LOGOUT_REDIRECT_KEY, window.location.href);
  auth.logout({
    clientID: AUTH_CLIENT_ID,
    returnTo: AUTH_LOGOUT_COMPLETE_URL,
  });
};

export const hasLoggedInFlag = () =>
  localStorage.getItem(LOGGED_IN_FLAG_KEY) === 'true';

export const register = () => {
  localStorage.setItem(LOGIN_REDIRECT_KEY, window.location.href);
  auth.authorize({ initial_screen: 'signUp' });
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};

export const redirectAfterLogIn = () => {
  const url = localStorage.getItem(LOGIN_REDIRECT_KEY) || '/account';
  setTimeout(() => {
    window.location.href = url;
  }, 1800);
};

export const redirectAfterLogOut = () => {
  const url = localStorage.getItem(LOGOUT_REDIRECT_KEY) || '/account';
  setTimeout(() => {
    window.location.href = url;
  }, 1800);
};
