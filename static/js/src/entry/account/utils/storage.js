import {
  LOGGED_IN_FLAG_KEY,
  CHANGED_EMAIL_FLAG_KEY,
  POST_LOG_OUT_REDIRECT_KEY,
  POST_LOGIN_REDIRECT_KEY,
} from '../constants';

// login
export const setLoggedInFlag = () => {
  localStorage.setItem(LOGGED_IN_FLAG_KEY, true);
};

export const getLoggedInFlag = () => localStorage.getItem(LOGGED_IN_FLAG_KEY);

export const clearLoggedInFlag = () => {
  localStorage.removeItem(LOGGED_IN_FLAG_KEY);
};

// changed email
export const setChangedEmail = email => {
  localStorage.setItem(CHANGED_EMAIL_FLAG_KEY, email);
};

export const getChangedEmail = () =>
  localStorage.getItem(CHANGED_EMAIL_FLAG_KEY);

export const clearChangedEmail = () => {
  localStorage.removeItem(CHANGED_EMAIL_FLAG_KEY);
};

// log out
export const setPostLogOutRedirect = () => {
  if (getChangedEmail()) {
    localStorage.setItem(POST_LOG_OUT_REDIRECT_KEY, '/account/changed-email/');
  } else {
    localStorage.setItem(POST_LOG_OUT_REDIRECT_KEY, '/donate');
  }
};

export const getPostLogOutRedirect = () =>
  localStorage.getItem(POST_LOG_OUT_REDIRECT_KEY);

export const clearPostLogOutRedirect = () => {
  localStorage.removeItem(POST_LOG_OUT_REDIRECT_KEY);
};

// log in
export const setPostLogInRedirect = () => {
  localStorage.setItem(POST_LOGIN_REDIRECT_KEY, '/account/');
};

export const getPostLogInRedirect = () =>
  localStorage.getItem(POST_LOGIN_REDIRECT_KEY);

export const clearPostLogInRedirect = () => {
  localStorage.removeItem(POST_LOGIN_REDIRECT_KEY);
};
