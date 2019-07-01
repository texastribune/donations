export class Auth0Error extends Error {
  constructor(message) {
    super(`Auth0 error: ${message}`);
  }
}

export class MultiplePersonsError extends Error {
  constructor() {
    super('Multiple persons returned from /persons/ endpoint');
  }
}

export class NoPersonsError extends Error {
  constructor() {
    super('Empty response from /persons/ endpoint');
  }
}

export class InvalidRouteError extends Error {
  constructor() {
    super('Invalid route');
  }
}
