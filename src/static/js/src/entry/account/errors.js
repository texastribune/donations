/* eslint-disable max-classes-per-file */

// think of as an abstract class
export class AppError extends Error {
  constructor({ name, message, extra }) {
    super(message);
    this.name = name;
    this.extra = extra;
  }
}

// can also be used in SSR
export class AxiosError extends AppError {
  constructor({ message, extra, status = 500 }) {
    super({ name: 'AxiosError', message, extra });
    this.status = status;
  }
}

// client only
export class UnverifiedError extends AppError {
  constructor({ extra } = {}) {
    super({
      name: 'UnverifiedError',
      message: 'Unverified email address accessing protected route',
      extra,
    });
  }
}

// client only
export class Auth0Error extends AppError {
  constructor({ message, extra }) {
    super({ name: 'Auth0Error', message, extra });
  }
}
