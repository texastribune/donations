import { captureException } from '@sentry/browser';

export default function logError(err, level = 'error') {
  captureException(err, level);
}
