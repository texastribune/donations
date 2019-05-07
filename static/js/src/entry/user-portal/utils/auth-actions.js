import auth from './auth';
import {
  LOGGED_IN_FLAG_KEY,
  AUTH_CLIENT_ID,
  AUTH_LOGOUT_COMPLETE_URL,
  LOGIN_REDIRECT_KEY,
  NON_STAFF_CONNECTION,
} from '../constants';

export const clearFlag = () => {
  localStorage.removeItem(LOGGED_IN_FLAG_KEY);
};

export const setFlag = () => {
  localStorage.setItem(LOGGED_IN_FLAG_KEY, true);
};

export const extractUser = authResult => {
  const keyMap = [
    ['nickname', 'nickname'],
    ['email', 'email'],
    ['email_verified', 'emailVerified'],
  ];
  const user = {};

  keyMap.forEach(group => {
    user[group[1]] = authResult[group[0]];
  });

  return user;
};

export const logIn = () => {
  localStorage.setItem(LOGIN_REDIRECT_KEY, window.location.href);
  auth.authorize({ initial_screen: 'login' });
};

export const logOut = () => {
  auth.logout({
    clientID: AUTH_CLIENT_ID,
    returnTo: AUTH_LOGOUT_COMPLETE_URL,
  });
};

export const isLoggedIn = () =>
  localStorage.getItem(LOGGED_IN_FLAG_KEY) === 'true';

export const register = () => {
  localStorage.setItem(LOGIN_REDIRECT_KEY, window.location.href);
  auth.authorize({ initial_screen: 'signUp' });
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};

export const redirectAfterLogIn = () => {
  const url = localStorage.getItem(LOGIN_REDIRECT_KEY) || '/';
  setTimeout(() => {
    window.location.href = url;
  }, 500);
};

export const redirectAfterLogOut = () => {
  setTimeout(() => {
    window.location.href = 'https://www.texastribune.org/';
  }, 500);
};
