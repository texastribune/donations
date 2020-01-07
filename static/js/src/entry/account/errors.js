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

export class AxiosError extends Error {
  constructor() {
    super('Axios error');
  }
}
