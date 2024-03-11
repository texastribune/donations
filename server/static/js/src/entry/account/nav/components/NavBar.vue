<template>
  <nav class="c-navbar c-navbar--light">
    <div class="c-navbar__top l-align-center-x">
      <a
        href="https://www.texastribune.org"
        class="c-navbar__logo l-align-center-self"
      >
        <img alt="The Texas Tribune" src="../../svg/tt.svg" />
      </a>

      <div class="c-navbar__content t-size-xxs t-uppercase t-lsp-m">
        <ul
          class="c-navbar__items c-navbar__items--no-space is-hidden-until-bp-l"
        >
          <li v-if="showUserLinks" class="c-navbar__item">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              active-class="is-active"
              exact
              ga-on="click"
              :to="{ name: 'accountOverview' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.home"
            >
              <strong>Account Overview</strong>
            </router-link>
          </li>
          <li v-if="showUserLinks && showMembershipLink" class="c-navbar__item">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              active-class="is-active"
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              <strong>Membership</strong>
            </router-link>
          </li>
          <li v-if="showUserLinks && showBlastLink" class="c-navbar__item">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              active-class="is-active"
              ga-on="click"
              :to="{ name: 'blast' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.blast"
            >
              <strong>The Blast</strong>
            </router-link>
          </li>
          <li class="c-navbar__item">
            <a
              href="/donate"
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              ga-on="click"
              :ga-event-category="ga.donations.category"
              :ga-event-action="ga.donations.actions['membership-intent']"
              :ga-event-label="ga.donations.labels.top"
            >
              <strong>Donate</strong>
            </a>
          </li>
          <li v-if="isLoggedIn" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-uppercase t-lsp-m"
              @click="logOut"
            >
              <strong>Log Out</strong>
            </button>
          </li>
          <li v-if="!isLoggedIn" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-uppercase t-lsp-m"
              @click="logIn"
            >
              <strong>Log In</strong>
            </button>
          </li>
        </ul>

        <ul class="c-navbar__items is-hidden-from-bp-l">
          <li v-if="!showDropdown" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable t-uppercase t-lsp-m"
              aria-label="Show menu"
              @click="toggleDropdown"
            >
              <icon name="bars" :display="{ size: 's' }" />
              <strong>&nbsp;Menu</strong>
            </button>
          </li>
          <li v-else class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable t-uppercase t-lsp-m"
              aria-label="Hide menu"
              @click="toggleDropdown"
            >
              <icon name="close" :display="{ size: 's' }" />
              <strong>&nbsp;Close</strong>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div
      v-if="showDropdown"
      class="c-navbar__dropdown is-hidden-from-bp-l t-size-xxs t-uppercase t-lsp-m"
    >
      <ul class="c-navbar__dropdown-items">
        <li v-if="showUserLinks" class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable"
            active-class="is-active"
            exact
            ga-on="click"
            :to="{ name: 'accountOverview' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.home"
          >
            <strong>Account Overview</strong>
          </router-link>
        </li>
        <li
          v-if="showUserLinks && showMembershipLink"
          class="c-navbar__dropdown-item"
        >
          <router-link
            class="c-navbar__clickable"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'membership' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.membership"
          >
            <strong>Membership</strong>
          </router-link>
        </li>
        <li v-if="showUserLinks" class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'edit-contact-info' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels['edit-contact-info']"
          >
            <strong>Profile Settings</strong>
          </router-link>
        </li>
        <li
          v-if="showUserLinks && showBlastLink"
          class="c-navbar__dropdown-item"
        >
          <router-link
            class="c-navbar__clickable"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'blast' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.blast"
          >
            <strong>The Blast</strong>
          </router-link>
        </li>
        <li class="c-navbar__dropdown-item">
          <a
            href="/donate"
            class="c-navbar__clickable"
            ga-on="click"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels.top"
          >
            <strong>Donate</strong>
          </a>
        </li>
        <li v-if="isLoggedIn" class="c-navbar__dropdown-item">
          <button
            class="c-navbar__clickable t-uppercase t-lsp-m"
            @click="logOut"
          >
            <strong>Log Out</strong>
          </button>
        </li>
        <li v-if="!isLoggedIn" class="c-navbar__dropdown-item">
          <button
            class="c-navbar__clickable t-uppercase t-lsp-m"
            @click="logIn"
          >
            <strong>Log In</strong>
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { logOut, logIn } from '../../utils/auth-actions';

export default {
  name: 'NavBar',

  props: {
    showUserLinks: {
      type: Boolean,
      required: true,
    },

    showBlastLink: {
      type: Boolean,
      default: false,
    },

    showMembershipLink: {
      type: Boolean,
      default: false,
    },

    isLoggedIn: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      showDropdown: false,
    };
  },

  methods: {
    logOut() {
      logOut();
    },

    logIn() {
      logIn();
    },

    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>
