import { captureException, withScope } from '@sentry/browser';

import { AxiosError } from '../errors';

export default function logError({ err, level = 'error' }) {
  withScope(scope => {
    if (err.extra) {
      scope.setExtra('extra', err.extra);
    }

    if (err instanceof AxiosError) {
      scope.setExtra('status', err.status);
    }

    captureException(err, level);
  });
}
