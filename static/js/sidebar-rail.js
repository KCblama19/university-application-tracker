/**
 * Desktop sidebar rail toggle.
 *
 * Bootstrap owns the mobile offcanvas sidebar.
 * This file only controls the desktop collapsed/expanded rail.
 *
 * The collapsed state is persisted in localStorage so navigating
 * between application pages does not reset the user's preference.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "sidebarCollapsed";
  var DESKTOP_BREAKPOINT = 992;

  var toggleButton = document.getElementById("sidebar-rail-toggle");

  if (!toggleButton) {
    return;
  }

  function isDesktop() {
    return window.innerWidth >= DESKTOP_BREAKPOINT;
  }

  function readSavedState() {
    try {
      return localStorage.getItem(STORAGE_KEY) === "true";
    } catch (error) {
      return false;
    }
  }

  function saveState(collapsed) {
    try {
      localStorage.setItem(STORAGE_KEY, String(collapsed));
    } catch (error) {
      // Storage may be unavailable in private browsing or
      // restrictive browser configurations. The UI still works.
    }
  }

  function applyCollapsedState(collapsed) {
    document.documentElement.classList.toggle("sidebar-collapsed", collapsed);

    toggleButton.setAttribute("aria-expanded", String(!collapsed));

    toggleButton.setAttribute(
      "aria-label",
      collapsed ? "Expand sidebar" : "Collapse sidebar",
    );

    toggleButton.setAttribute(
      "title",
      collapsed ? "Expand sidebar" : "Collapse sidebar",
    );
  }

  /*
   * Restore the saved state only on desktop.
   *
   * Mobile uses Bootstrap's offcanvas drawer and should never
   * inherit the desktop rail state.
   */
  if (isDesktop()) {
    applyCollapsedState(readSavedState());
  }

  toggleButton.addEventListener("click", function () {
    if (!isDesktop()) {
      return;
    }

    var collapsed =
      !document.documentElement.classList.contains("sidebar-collapsed");

    applyCollapsedState(collapsed);
    saveState(collapsed);
  });

  var lastIsDesktop = isDesktop();

  window.addEventListener("resize", function () {
    var nowDesktop = isDesktop();

    if (nowDesktop === lastIsDesktop) {
      return;
    }

    lastIsDesktop = nowDesktop;

    if (nowDesktop) {
      applyCollapsedState(readSavedState());
    } else {
      /*
       * Remove the desktop rail state before entering mobile.
       * Bootstrap can then control the offcanvas normally.
       */
      document.documentElement.classList.remove("sidebar-collapsed");
    }
  });
})();
