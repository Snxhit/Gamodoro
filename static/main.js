const input = document.querySelector("input[name='username']");
if (input) {
  input.value = localStorage.getItem("username") || "";

  input.addEventListener("input", () => {
    localStorage.setItem("username", input.value);
  });
}
