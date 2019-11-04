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

export class AxiosNetworkError extends Error {
  constructor(xhr) {
    super('Axios network error');

    const {
      status,
      statusText,
      timeout,
      readyState,
      response,
      responseText,
      responseType,
      responseURL,
    } = xhr;

    const metadata = {
      status,
      statusText,
      timeout,
      readyState,
      response,
      responseText,
      responseType,
      responseURL,
    };

    this.metadata = JSON.stringify(metadata);
  }
}
