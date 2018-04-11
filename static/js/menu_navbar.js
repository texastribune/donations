import { BREAKPOINTS, SHOW_HIDE_CLASSES } from './constants';
import debounce from './utils/debounce';

const $mobileDropdown = $('#mobile-dropdown');
const $menuMobileFullLogo = $('#menu-mobile-full-logo');
const $menuMobileSocials = $('#menu-mobile-social');
const $menuOpen = $('#menu-open');
const $menuClose = $('#menu-close');
const $menuSearchForm = $('#menu-search-form');
const $menuSearchOpen = $('#menu-search-open');
const $menuSearchClose = $('#menu-search-close');
const $menuSearchInput = $('#site-search-q');

let currWindowWidth = $(window).width();

export default function bindMenuEvents() {
  const whichResize = afterResize;

  bindShowMobileDropdown();
  bindHideMobileDropdown();
  bindShowSearch();
  bindHideSearch();
  window.addEventListener('resize', debounce(whichResize, 500, false));
  window.addEventListener('orientationchange', debounce(afterOrientationChange, 500, false));
}

// exported because it's included as a method in mainBundle
export function toggleMobileDropdown() {
  if (dropdownIsVisible()) {
    hideMobileDropdown();
  } else {
    showMobileDropdown();
  }
}

// returns true if the mobile dropdown is visible
function dropdownIsVisible() {
  return !$mobileDropdown.hasClass(SHOW_HIDE_CLASSES.hideUntilLarge);
}

// show the mobile dropdown
function showMobileDropdown() {
  $mobileDropdown.removeClass(SHOW_HIDE_CLASSES.hideUntilLarge);
  $menuOpen.addClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuClose.removeClass(SHOW_HIDE_CLASSES.hideAlways);
}

// hide the mobile dropdown
function hideMobileDropdown() {
  $mobileDropdown.addClass(SHOW_HIDE_CLASSES.hideUntilLarge);
  $menuOpen.removeClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuClose.addClass(SHOW_HIDE_CLASSES.hideAlways);
  closeSearch();
}

function showSearch() {
  $menuSearchForm.removeClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuSearchOpen.addClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuSearchClose.removeClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuSearchInput.focus();

  if(!$menuSearchForm.hasClass('thin')) {
    resetMenu();
  }
}

function closeSearch() {
  $menuSearchForm.addClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuSearchClose.addClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuSearchOpen.removeClass(SHOW_HIDE_CLASSES.hideAlways);
}

// show the mobile dropdown when "menu" is clicked/tapped
function bindShowMobileDropdown() {
  $menuOpen.click(function(e) {
    e.preventDefault();
    showMobileDropdown();
  });
}

// hide the mobile dropdown when "close" is clicked/tapped
function bindHideMobileDropdown() {
  $menuClose.click(function(e) {
    e.preventDefault();
    hideMobileDropdown();
  });
}

// show the search form when "Search" is clicked/tapped
function bindShowSearch() {
  $menuSearchOpen.click(function(e) {
    e.preventDefault();
    showSearch();
  });
}

// hide the search form when "close" on search bar is clicked/tapped
function bindHideSearch() {
  $menuSearchClose.click(function(e) {
    e.preventDefault();
    closeSearch();
  });
}

function shouldResetMenu(newWindowWidth) {
  return (
    (currWindowWidth >= BREAKPOINTS.m && newWindowWidth < BREAKPOINTS.m) ||
    (currWindowWidth < BREAKPOINTS.m && newWindowWidth >= BREAKPOINTS.m)
  );
}

function updateCurrWindowWidth(newWindowWidth) {
  currWindowWidth = newWindowWidth;
}

// if mobile social buttons do not exist
// maybe reset the menu
const afterResize = function() {
  const newWindowWidth = $(window).width();

  if (shouldResetMenu(newWindowWidth)) {
    resetMenu();
  }

  updateCurrWindowWidth(newWindowWidth);
};

// on orientationchange, reset the menu
const afterOrientationChange = function() {
  resetMenu();
  updateCurrWindowWidth($(window).width());
};

// hide the mobile socials, show the TT logo, hide the mobile dropdown
function resetMenu() {
  $menuMobileSocials.addClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuMobileFullLogo.removeClass(SHOW_HIDE_CLASSES.hideAlways);
  $mobileDropdown.addClass(SHOW_HIDE_CLASSES.hideUntilLarge);
  $menuOpen.removeClass(SHOW_HIDE_CLASSES.hideAlways);
  $menuClose.addClass(SHOW_HIDE_CLASSES.hideAlways);
}
