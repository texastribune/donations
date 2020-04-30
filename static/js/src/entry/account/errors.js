const AUTH0_STATUS_MAP = {
  invalid_request: 400,
  unauthorized_client: 401,
  unsupported_credential_type: 400,
  access_denied: 403,
  blocked_user: 403,
  password_leaked: 401,
  too_many_attempts: 429,
};

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

export class Auth0Error extends AppError {
  constructor({ message, code }) {
    super({
      name: 'Auth0Error',
      status: AUTH0_STATUS_MAP[code],
      message,
    });
  }
}
