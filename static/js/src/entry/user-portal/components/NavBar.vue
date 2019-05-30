<template>
  <nav class="c-navbar has-bg-white">
    <div class="c-navbar__top c-navbar__top--standard">
      <a href="https://www.texastribune.org" class="c-navbar__logo">
        <img
          alt="The Texas Tribune"
          src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAxNy4xLjAsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDApICAtLT4NCjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+DQo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB2aWV3Qm94PSIwIDAgNTAwIDU1LjA3NCIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTAwIDU1LjA3NCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+DQoJPGc+DQoJCTxnPg0KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTcyLjUxMSw4LjczdjM5LjE0NGgtOC43OTlWOC43M2gtOC42NlYwLjk4N2gyNi4wNDlWOC43M0g3Mi41MTF6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTAyLjUxLDQ3Ljg3NFYyOC42NTVoLTkuNzg2djE5LjIxOWgtOC43MjlWMC45ODdoOC43Mjl2MTkuODU1aDkuNzg2VjAuOTg3aDguODAxdjQ2Ljg4N0gxMDIuNTF6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTE2Ljc2Miw0Ny44NzRWMC45ODdoMjIuMzg3djcuNTMySDEyNS40OXYxMS42MTdoOS40MzR2Ni45aC05LjQzNHYxMy4wMjNoMTMuNjU5djcuODE1SDExNi43NjJ6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMTY5LjU2LDguNzN2MzkuMTQ0aC04LjgwMVY4LjczaC04LjY2VjAuOTg3aDI2LjA0OVY4LjczSDE2OS41NnoiLz4NCgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0xODEuOTE4LDQ3Ljg3NFYwLjk4N2gyMi4zODl2Ny41MzJoLTEzLjY1OHYxMS42MTdoOS40MzN2Ni45aC05LjQzM3YxMy4wMjNoMTMuNjU4djcuODE1SDE4MS45MTh6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMjI2Ljk4MSw0Ny44NzRsLTUuNDkyLTE2LjE5MWwtNS45ODMsMTYuMTkxaC04LjUxOWw5LjY0NS0yMy42NTZMMjA3LjU1LDAuOTg3aDkuMTUzbDUuMTM4LDE2LjE5MQ0KCQkJCWw1LjYzMy0xNi4xOTFoOC41OWwtOS4zNjMsMjIuNTI5bDkuNDMzLDI0LjM1OEgyMjYuOTgxeiIvPg0KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTI1Ny41NTgsNDcuODc0bC0xLjU1LTkuMjIxaC04LjMwN2wtMS42OSw5LjIyMWgtOC4xNjdsOS40MzQtNDYuODg3aDkuNzg2bDkuMzYzLDQ2Ljg4N0gyNTcuNTU4eg0KCQkJCSBNMjUyLjA2NiwxMy42NTlsLTMuMTY5LDE4LjA5NGg1Ljk4NEwyNTIuMDY2LDEzLjY1OXoiLz4NCgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0yODAuNTc0LDQ4LjkzYy04LjAyNiwwLTEzLjAyNC00Ljc4NS0xMy4wMjQtMTIuMTA5di0zLjIzOGg4LjAyNnYyLjc0NmMwLDMuNDQ5LDEuNjE5LDUuMzUyLDQuNzg4LDUuMzUyDQoJCQkJYzMuMDk4LDAsNC42NDYtMS44MzIsNC42NDYtNC43MThjMC0zLjczMS0yLjM5NC02LjI2NS03LjA0MS05LjcxNWMtNC43ODYtMy40NS05Ljk5Ni04LjA5Ni05Ljk5Ni0xNC42NDINCgkJCQlDMjY3Ljk3Miw1Ljg0NCwyNzIuMzM3LDAsMjgwLjc4NSwwYzcuMzkzLDAsMTIuMzIxLDUuMDcsMTIuMzIxLDEyLjA0djMuMDI3aC03Ljk1NnYtMi44MTdjMC0yLjg4Ni0xLjQ3Ni00Ljk5OC00LjQzNC00Ljk5OA0KCQkJCWMtMi41MzQsMC00LjIyNSwxLjYxOS00LjIyNSw0LjIyNWMwLDMuOTQyLDIuMzIzLDUuOTg0LDcuNTMyLDkuNzg2YzUuNTY0LDQuMTUzLDkuNTA2LDguMzc4LDkuNTA2LDE0LjcxNQ0KCQkJCUMyOTMuNTI4LDQzLjUxLDI4OC4zMTksNDguOTMsMjgwLjU3NCw0OC45M3oiLz4NCgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0zMjIuNTUyLDguNzN2MzkuMTQ0aC04LjhWOC43M2gtOC42NjFWMC45ODdoMjYuMDUxVjguNzNIMzIyLjU1MnoiLz4NCgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0zNTYuNDY3LDQ4LjE1N2MtMy40NSwwLTQuNzg4LTIuODE3LTQuNzg4LTYuOXYtOC44YzAtMi4xODItMS4xMjctNC4wMTMtMy41OS00LjAxM2gtNC41NzZ2MTkuNDMxaC04LjczDQoJCQkJVjAuOTg3aDE0LjQzMmM2LjQwNSwwLDEwLjcsMy42NjIsMTAuNywxMC4yMDd2Ni42MmMwLDMuNTE4LTEuNjE5LDYuMTI0LTUuMjc5LDcuMjVjMy42NTksMC45ODcsNS40Miw0LjA4Myw1LjQyLDcuMTExdjguNTkNCgkJCQljMCwyLjE4MywwLjYzMywzLjY1OSwxLjY5MSw0Ljc4NnYyLjYwNkgzNTYuNDY3eiBNMzUxLjM5NywxMS41NDZjMC0yLjExMS0wLjkxNS0zLjM4LTMuMDk3LTMuMzhoLTQuNzg2djEzLjhoNC40MzYNCgkJCQljMi4yNTIsMCwzLjQ0Ny0xLjE5OCwzLjQ0Ny0zLjczMVYxMS41NDZ6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMzY2LjkxNSw0Ny44NzRWMC45ODdoOC43MzF2NDYuODg3SDM2Ni45MTV6Ii8+DQoJCQk8cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMzk3LjQ2NSw0Ny44NzRoLTE0Ljc4M1YwLjk4N2gxNC42NDRjNi40MDcsMCwxMC4zNDksMy40NSwxMC4zNDksOS45Mjh2NS4wNjgNCgkJCQljMCw0LjAxMy0xLjU1LDcuMDQyLTUuNTYyLDcuODg0YzQuMjI2LDEuMTI4LDUuNzczLDQuMDE0LDUuNzczLDcuOTU4djYuMTI0QzQwNy44ODYsNDQuNDk2LDQwMy44NzIsNDcuODc0LDM5Ny40NjUsNDcuODc0eg0KCQkJCSBNMzk5LjI5NywxMS41NDZjMC0yLjExMS0wLjkxNi0zLjM4LTMuMDk5LTMuMzhoLTQuNzE2djEyLjg4NWg0LjM2NGMyLjI1NCwwLDMuNDUxLTEuMTk4LDMuNDUxLTMuNjYyVjExLjU0NnogTTM5OS40MzcsMzEuMTkxDQoJCQkJYzAtMi40NjUtMS4xOTYtMy43MzEtMy40NDktMy43MzFoLTQuNTA2djEzLjIzNWg0LjkyOGMyLjE4MywwLDMuMDI3LTEuMTk4LDMuMDI3LTMuMzc5VjMxLjE5MXoiLz4NCgkJCTxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik00MjYuMjc5LDQ4LjkzYy03LjYwNCwwLTEzLjIzNi00Ljg1Ny0xMy4yMzYtMTEuODk5VjAuOTg3aDguODd2MzYuMDQ1YzAsMi43NDYsMS41NDgsNC4yOTcsNC4zNjYsNC4yOTcNCgkJCQljMi44ODYsMCw0LjQzNC0xLjU1MSw0LjQzNC00LjI5N1YwLjk4N2g4LjUxOHYzNi4wNDVDNDM5LjIzMSw0NC4wNzMsNDMzLjg4MSw0OC45Myw0MjYuMjc5LDQ4LjkzeiIvPg0KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTQ2NC45NjcsNDcuODc0bC05LjA4My0xOS45OTRsLTMuMzA5LTcuNDYydjI3LjQ1NWgtOC4wMjdWMC45ODdoNy41MzVsOC42NTgsMjAuMzQ2bDMuMDk5LDcuNDYzVjAuOTg3DQoJCQkJaDcuODg2djQ2Ljg4N0g0NjQuOTY3eiIvPg0KCQkJPHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTQ3Ny42MTMsNDcuODc0VjAuOTg3SDUwMHY3LjUzMmgtMTMuNjU4djExLjYxN2g5LjQzNHY2LjloLTkuNDM0djEzLjAyM0g1MDB2Ny44MTVINDc3LjYxM3oiLz4NCgkJPC9nPg0KCQk8cGF0aCBmaWxsPSIjRkVCRjEwIiBkPSJNMCwwLjUwOXY1NC41NjVsMTAuOTczLTYuODU5aDM2LjczM1YwLjUwOUgweiBNMzQuMTY1LDM4LjYwOWwtMTAuNDUtNi44NzVsLTEwLjQ0OCw2Ljg3NWwzLjMxLTEyLjA2DQoJCQlsLTkuNzY3LTcuODEybDEyLjQ5My0wLjU4bDQuNDEyLTExLjcwM2w0LjQxMiwxMS43MDNsMTIuNDkzLDAuNThsLTkuNzY3LDcuODEyTDM0LjE2NSwzOC42MDl6Ii8+DQoJPC9nPg0KPC9zdmc+DQo="
        />
      </a>

      <div class="c-navbar__content">
        <ul class="c-navbar__items is-hidden-until-bp-l">
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              :to="{ name: 'home' }"
              >Account Overview</router-link
            >
          </li>
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              :to="{ name: 'membership' }"
              >Membership</router-link
            >
          </li>
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              :to="{ name: 'blast' }"
              >The Blast</router-link
            >
          </li>
          <li class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated"
              @click="user.logOut"
            >
              Log Out
            </button>
          </li>
        </ul>

        <ul class="c-navbar__items is-hidden-from-bp-l">
          <li v-if="!showDropdown" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable"
              aria-label="Show menu"
              @click="toggleDropdown"
            >
              <icon name="bars" :display="{ size: 's' }" />
              <span>&nbsp;Menu</span>
            </button>
          </li>
          <li v-else class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable"
              aria-label="Hide menu"
              @click="toggleDropdown"
            >
              <icon name="close" :display="{ size: 's' }" />
              <span>&nbsp;Close</span>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="showDropdown" class="c-navbar__dropdown is-hidden-from-bp-l">
      <ul class="c-navbar__dropdown-items">
        <li class="c-navbar__dropdown-item">
          <router-link class="c-navbar__clickable" :to="{ name: 'home' }"
            >Account Overview</router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <router-link class="c-navbar__clickable" :to="{ name: 'membership' }"
            >Membership</router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <router-link class="c-navbar__clickable" :to="{ name: 'blast' }"
            >The Blast</router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <button class="c-navbar__clickable" @click="user.logOut">
            Log Out
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import userMixin from '../mixins/user';

export default {
  name: 'NavBar',

  mixins: [userMixin],

  data() {
    return {
      showDropdown: false,
    };
  },

  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>
