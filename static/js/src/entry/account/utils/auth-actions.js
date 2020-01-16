import auth from './auth';
import {
  AUTH_PORTAL_CLIENT_ID,
  AUTH_PORTAL_LOGOUT_COMPLETE_URL,
  AUTH_PORTAL_LOGIN_COMPLETE_URL,
  NON_STAFF_CONNECTION,
  DONATE_REDIRECT,
  ACCOUNT_HOME_REDIRECT,
  REDIRECTS,
} from '../constants';

const createRedirectQueryParams = ({ next, data }) => {
  let queryParams = `next=${next}`;

  if (data) {
    queryParams += `&data=${encodeURIComponent(JSON.stringify(data))}`;
  }

  return queryParams;
};

export const logIn = (info = {}) => {
  const queryParams = createRedirectQueryParams({
    next: ACCOUNT_HOME_REDIRECT,
    ...info,
  });

  auth.authorize({
    initial_screen: 'login',
    redirectUri: `${AUTH_PORTAL_LOGIN_COMPLETE_URL}?${queryParams}`,
  });
};

export const logOut = (info = {}) => {
  const queryParams = createRedirectQueryParams({
    next: DONATE_REDIRECT,
    ...info,
  });

  auth.logout({
    clientID: AUTH_PORTAL_CLIENT_ID,
    returnTo: `${AUTH_PORTAL_LOGOUT_COMPLETE_URL}?${queryParams}`,
  });
};

export const redirect = routeQueryParams => {
  const { next, data } = routeQueryParams;
  let url = REDIRECTS[next];

  if (url) {
    if (data) {
      const parsedData = JSON.parse(decodeURIComponent(data));

      url += `?${Object.keys(parsedData).reduce(
        (acc, curr, index) =>
          `${acc}${index === 0 ? '' : '&'}${curr}=${parsedData[curr]}`,
        ''
      )}`;
    }

    setTimeout(() => {
      window.location.href = url;
    }, 1800);
  }
};

export const resetPassword = (email, cb) => {
  auth.changePassword({ email, connection: NON_STAFF_CONNECTION }, cb);
};
