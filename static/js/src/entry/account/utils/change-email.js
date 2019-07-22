import { CHANGED_EMAIL_FLAG_KEY } from '../constants';

export const setChangedEmailFlag = email => {
  localStorage.setItem(CHANGED_EMAIL_FLAG_KEY, email);
};

export const clearChangedEmailFlag = () => {
  localStorage.removeItem(CHANGED_EMAIL_FLAG_KEY);
};

export const hasChangedEmailFlag = () =>
  localStorage.getItem(CHANGED_EMAIL_FLAG_KEY);
