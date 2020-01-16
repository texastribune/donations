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
  constructor({ extra, status, headers, data }) {
    super('Axios response error');

    this.extra = extra;

    if (status) this.status = status;
    if (headers) this.headers = headers;
    if (data) this.data = data;
  }
}

export class AxiosRequestError extends Error {
  constructor({ extra }) {
    super('Axios request error');

    this.extra = extra;
  }
}
