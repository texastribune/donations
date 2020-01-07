export default function logPageView() {
  window.dataLayer.push({
    event: 'userPortalPageview',
    pagePath: window.location.pathname,
    pageTitle: document.title,
  });
}
