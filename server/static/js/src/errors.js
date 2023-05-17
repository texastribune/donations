/* eslint-disable max-classes-per-file */

// from: https://github.com/coralproject/talk/blob/v4.10.3/errors.js
class ExtendableError {
  constructor(message = null) {
    this.message = message;
    this.stack = new Error(message).stack;
  }
}

export class RecaptchaError extends ExtendableError {
  constructor() {
    super('Failed to get recaptcha token');
  }
}

export class StripeError extends ExtendableError {
  constructor(message, type) {
    super(message);
    this.type = type;
  }
}
