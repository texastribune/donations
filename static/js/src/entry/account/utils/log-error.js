import { captureException, withScope } from '@sentry/browser';

export default function logError(err, level = 'error') {
  withScope(scope => {
    scope.setExtra('pageTitle', document.title);
    captureException(err, level);
  });
}
