{pkgs, ...}: {
  languages.python = {
    enable = true;
    libraries = with pkgs; [cairo];
    venv.enable = true;
    venv.requirements = builtins.readFile ./docs/requirements.txt;
  };

  languages.javascript = {
    enable = true;
    directory = "./docs";
    npm = {
      enable = true;
      install.enable = true;
    };
  };
}
