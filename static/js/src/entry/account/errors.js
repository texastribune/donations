export class Auth0Error extends Error {
  constructor(message) {
    super(`Auth0 error: ${message}`);
  }
}

export class UnverifiedError extends Error {
  constructor() {
    super('Unverified email address');
  }
}

export class InvalidRouteError extends Error {
  constructor() {
    super('Invalid route');
  }
}

export class AxiosResponseError extends Error {
  constructor({ status, headers, data, extra }) {
    super('Axios response error');

    this.status = status;
    this.headers = headers;
    this.data = data;
    this.extra = extra;
  }
}

export class AxiosRequestError extends Error {
  constructor({ extra }) {
    super('Axios request error');

    this.extra = extra;
  }
}
