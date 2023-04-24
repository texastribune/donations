import DOMPurify from 'dompurify';

export default function sanitizeParams(params) {
  const sanitized = {};

  Object.keys(params).forEach(key => {
    sanitized[key] = DOMPurify.sanitize(params[key]);
  });

  return sanitized;
}
