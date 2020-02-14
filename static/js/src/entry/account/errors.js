export class AppError extends Error {
  constructor({ name, message, status = 500, meta = {} }) {
    super(message);

    this.name = name;
    this.status = status;
    this.meta = meta;
  }
}

export class NetworkError extends AppError {
  constructor({ message, status = 500, meta = {} }) {
    super({ name: 'NetworkError', message, status, meta });
  }
}

export class UnverifiedError extends AppError {
  constructor() {
    super({
      name: 'UnverifiedError',
      message: 'Unverified email address accessing protected route',
      status: 403,
    });
  }
}

export class Auth0Error extends Error {
  constructor(message) {
    super(`Auth0 error: ${message}`);
  }
}
