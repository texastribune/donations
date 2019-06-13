export class LoggedOutError extends Error {
  constructor() {
    super('Logged out');
  }
}

export class Auth0Error extends Error {
  constructor() {
    super('Auth0 error');
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
