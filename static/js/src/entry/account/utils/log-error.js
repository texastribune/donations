import { captureException, withScope } from '@sentry/browser';

export default function logError(err, level = 'error') {
  if (err.metadata) {
    // eslint-disable-next-line prefer-arrow-callback
    withScope(function callback(scope) {
      scope.setExtra(err.metadata);
      captureException(err, level);
    });
  } else {
    captureException(err, level);
  }
}
