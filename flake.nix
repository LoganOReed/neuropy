{
  description = "Python application packaged using poetry2nix";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      # create a custom "mkPoetryApplication" API function that under the hood uses
      # the packages and versions (python3, poetry etc.) from our pinned nixpkgs above:
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      myPythonApp = mkPoetryApplication {
        projectDir = ./.;
        python = pkgs.python39;
        preferWheels = true;
        nativeBuildInputs = [ pkgs.makeWrapper ];
        propogatedBuildInputs = [ pkgs.ffmpeg ];
        postInstall = ''
              wrapProgram "$out/bin/extrap" \
                --prefix PATH : ${nixpkgs.lib.makeBinPath [ pkgs.ffmpeg ]}
            '';
        };
    in
    {
      # Right now just change program when using another one 
      apps.${system}.default = {
        type = "app";
        nativeBuildInputs = [ pkgs.makeWrapper ];
        propogatedBuildInputs = [ pkgs.ffmpeg ];
        program = "${myPythonApp}/bin/extrap";
      };
    };
}
