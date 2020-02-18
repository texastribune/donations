export default function logPageView() {
  window.dataLayer.push({
    event: 'userPortalPageview',
    pageTitle: document.title,
    pagePath: window.location.pathname,
  });
}
