{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  # https://devenv.sh/packages/
  packages = [
    pkgs.pre-commit
    pkgs.black
    pkgs.python311Packages.flake8
  ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    version = "3.11";
    venv = {
      enable = true;
      requirements = ./src/scheduler/requirements.txt;
    };
  };

  # https://devenv.sh/basics/
  enterShell = ''
    python --version
  '';
}
