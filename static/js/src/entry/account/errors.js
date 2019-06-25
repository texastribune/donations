export class Auth0Error extends Error {
  constructor(message) {
    super(`Auth0 error: ${message}`);
  }
}

export class MultiplePersonsError extends Error {
  constructor() {
    super('Multiple persons');
  }
}

export class NoPersonsError extends Error {
  constructor() {
    super('No persons');
  }
}

export class InvalidRouteError extends Error {
  constructor() {
    super('Invalid route');
  }
}
