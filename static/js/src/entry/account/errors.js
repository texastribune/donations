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
