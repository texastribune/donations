import { RecaptchaError } from '../errors';
import { RECAPTCHA_KEY } from '../constants';

export default function getRecaptchaToken(action) {
  const { grecaptcha } = window;

  return new Promise((resolve, reject) => {
    try {
      grecaptcha.ready(() => {
        grecaptcha
          // eslint-disable-next-line no-underscore-dangle
          .execute(RECAPTCHA_KEY, {
            action,
          })
          .then(token => {
            resolve(token);
          });
      });
    } catch (err) {
      reject(new RecaptchaError());
    }
  });
}
