<template>
  <footer class="c-site-footer has-bg-black-off has-xl-padding">
    <div
      class="c-site-footer__inner l-container--xl l-align-center-x"
      style="max-width: 1080px;"
    >
      <div class="c-site-footer__logo-col">
        <span class="c-site-footer__logo c-icon has-text-yellow">
          <svg aria-hidden="true" focusable="false">
            <use xlink:href="#bug"></use>
          </svg>
        </span>
      </div>

      <div class="c-site-footer__account-col t-size-xs">
        <h4
          class="c-site-footer__header has-text-yellow t-uppercase has-xs-btm-marg"
        >
          Your account
        </h4>
        <ul class="c-site-footer__links">
          <li>
            <router-link :to="{ name: 'home' }">Account Overview</router-link>
          </li>
          <li>
            <router-link :to="{ name: 'membership' }"
              >Membership Status</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'payments' }"
              >Donation History</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'blast' }"
              >The Blast Newsletter</router-link
            >
          </li>
          <li>
            <router-link :to="{ name: 'blast-payments' }"
              >The Blast Payment History</router-link
            >
          </li>
        </ul>
      </div>

      <div class="c-site-footer__info-col t-size-xs">
        <h4
          class="c-site-footer__header has-text-yellow t-uppercase has-xs-btm-marg"
        >
          Info
        </h4>
        <ul class="c-site-footer__links">
          <li>
            <a href="https://www.texastribune.org/about/community-guidelines/"
              >Community Guidelines</a
            >
          </li>
          <li><a href="/donate">About Membership</a></li>
          <li>
            <a href="https://www.texastribune.org/about/privacy-policy/"
              >Privacy Policy</a
            >
          </li>
          <li><a href="https://www.texastribune.org/">texastribune.org</a></li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'SiteFooter',
};
</script>
