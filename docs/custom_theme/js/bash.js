terminal("#terminal-index", [
  { type: "input", value: 'python -m pip install "fastberry[testing]"' },
  { type: "progress", value: 100 },
  { value: "Successfully installed fastberry", startDelay: 0 },
]);

terminal("#terminal-getting-started", [
  { type: "input", value: "pdm init" },
  { value: "0. C:\\Python311\\python.EXE (3.11)", startDelay: 0 },
  {
    value: "1. C:\\Users\\Me\\etc...\\python3.10.exe (3.10)",
    startDelay: 0,
  },
  {
    value: "2. C:\\Users\\Me\\etc...\\python3.7.exe (3.7)",
    startDelay: 0,
  },
  { type: "input", typeDelay: 1000, prompt: "Please select (0):", value: "1" },
  {
    value: " ",
    startDelay: 0,
  },
  {
    value: "Using Python interpreter: C:\\etc...\\python3.10.exe (3.10)",
    startDelay: 0,
  },
  {
    type: "input",
    typeDelay: 1000,
    prompt: "Would you like to create a virtualenv ... [y/n] (y):",
    value: "y",
  },
  {
    value: "Virtualenv is created successfully at C:\\etc...",
    startDelay: 0,
  },
]);

terminal("#terminal-getting-started-2", [
  {
    value: "Is the project a library that will be uploaded to PyPI [y/n] (n):",
    startDelay: 0,
  },
  {
    value: "License(SPDX name) (MIT):",
    startDelay: 0,
  },
  {
    value: "Author name (me):",
    startDelay: 0,
  },
  {
    value: "Author email (me@example.com):",
    startDelay: 0,
  },

  {
    value: "Changes are written to pyproject.toml.",
    startDelay: 0,
  },
]);

terminal("#terminal-getting-started-3", [
  {
    type: "input",
    value: 'pdm add "fastberry[testing]"',
    startDelay: 0,
  },
  {
    value: "Adding packages to default dependencies: fastberry",
    startDelay: 0,
  },
  { type: "progress", value: 100 },
  {
    value: "🎉 All complete!",
    startDelay: 0,
  },
]);
