import { LOGGED_IN_FLAG_KEY } from '../constants';

export const setLoggedInFlag = () => {
  localStorage.setItem(LOGGED_IN_FLAG_KEY, true);
};

export const getLoggedInFlag = () => localStorage.getItem(LOGGED_IN_FLAG_KEY);

export const clearLoggedInFlag = () => {
  localStorage.removeItem(LOGGED_IN_FLAG_KEY);
};
