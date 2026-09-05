function setDailyGreeting() {
  const hour = new Date().getHours();

  let greeting = "Hello";

  if (hour < 12) {
    greeting = "Good morning";
  } else if (hour < 17) {
    greeting = "Good afternoon";
  } else if (hour < 21) {
    greeting = "Good evening";
  } else {
    greeting = "Good night";
  }

  const greetingElement = document.getElementById("welcome-greeting");

  if (!greetingElement) {
    return;
  }

  const username = greetingElement.dataset.username || "Guest";

  greetingElement.textContent = `${greeting}, ${username}.`;
}

document.addEventListener("DOMContentLoaded", setDailyGreeting);
