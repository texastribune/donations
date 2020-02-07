export default function logPageView({ pagePath, pageTitle }) {
  window.dataLayer.push({
    event: 'userPortalPageview',
    pageTitle,
    pagePath,
  });
}
