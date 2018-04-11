export const BREAKPOINTS = {
  xs: 320,
  s: 520,
  m: 650,
  l: 845,
  xl: 1080,
  xxl: 1300,
  default: 960,
};

export const SHOW_HIDE_CLASSES = {
  hideFromSmall: 'hide_from--s',
  hideFromLarge: 'hide_from--l',
  hideUntilSmall: 'hide_until--s',
  hideUntilLarge: 'hide_until--l',
  hideUntilMedium: 'hide_until--m',
  hideAlways: 'hidden',
};

export const LOADING_CLASSES = {
  small: 'loading--s',
};

export const DJANGO_URLS = {
  accountEdit: '/accounts/edit/',
  logIn: '/accounts/login/',
  logOut: '/accounts/logout/',
  register: '/accounts/register/',
};

export const GLOBAL_OBJECT_NAME = 'ttGlobal';

export const LIBRARY = 'jsBundle';

export const STATIC_PATH = '/static/';

export const SERIES_SLUGS = {
  harvey: 'in-harveys-wake',
};

export const ENV = {
  isTest: process.env.NODE_ENV === 'test',
};
