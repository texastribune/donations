export class AppError extends Error {
  constructor({ name, message, extra = {} }) {
    super(message);
    this.name = name;
    this.extra = extra;
  }
}

export class AxiosError extends AppError {
  constructor({ message, status = null, extra = {} }) {
    super({ name: 'AxiosError', message, extra });
    this.status = status;
  }
}

export class UnverifiedError extends AppError {
  constructor() {
    super({
      name: 'UnverifiedError',
      message: 'Unverified email address accessing protected route',
    });
  }
}

export class Auth0Error extends AppError {
  constructor({ message }) {
    super({
      name: 'Auth0Error',
      message,
    });
  }
}
