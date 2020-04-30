import { captureException, withScope } from '@sentry/browser';

export default function logError({ err, level = 'error' }) {
  withScope(scope => {
    if (err.meta) {
      scope.setExtra('meta', err.meta);
    }

    if (err.status) {
      scope.setExtra('status', err.status);
    }

    captureException(err, level);
  });
}
