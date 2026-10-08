<div align="center">

# GitHub themes for Otty

GitHub's official [VS Code themes](https://github.com/primer/github-vscode-theme), all nine of them, for the [Otty](https://otty.sh) terminal.

[![CI](https://github.com/kingsleydon/otty-github-theme/actions/workflows/ci.yml/badge.svg)](https://github.com/kingsleydon/otty-github-theme/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<img src="assets/previews/github-dark-default.svg" alt="GitHub Dark Default in Otty" width="760">

</div>

## Install

**One theme:** click **Download** under a theme below, open the file, and choose **Import & Apply**.

**All themes:** paste this into Otty:

```sh
curl -fsSL https://raw.githubusercontent.com/kingsleydon/otty-github-theme/main/install.sh | sh
```

Then pick one in **Settings → Appearance → Themes**. Run it again any time to update.

## Themes

<table>
<tr>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-default.ottytheme"><img src="assets/previews/github-dark-default.svg" alt="GitHub Dark Default"></a><br><b>GitHub Dark Default</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-default.ottytheme">Download</a></td>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-default.ottytheme"><img src="assets/previews/github-light-default.svg" alt="GitHub Light Default"></a><br><b>GitHub Light Default</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-default.ottytheme">Download</a></td>
</tr>
<tr>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-dimmed.ottytheme"><img src="assets/previews/github-dark-dimmed.svg" alt="GitHub Dark Dimmed"></a><br><b>GitHub Dark Dimmed</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-dimmed.ottytheme">Download</a></td>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-high-contrast.ottytheme"><img src="assets/previews/github-light-high-contrast.svg" alt="GitHub Light High Contrast"></a><br><b>GitHub Light High Contrast</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-high-contrast.ottytheme">Download</a></td>
</tr>
<tr>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-high-contrast.ottytheme"><img src="assets/previews/github-dark-high-contrast.svg" alt="GitHub Dark High Contrast"></a><br><b>GitHub Dark High Contrast</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-high-contrast.ottytheme">Download</a></td>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-colorblind.ottytheme"><img src="assets/previews/github-light-colorblind.svg" alt="GitHub Light Colorblind"></a><br><b>GitHub Light Colorblind</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light-colorblind.ottytheme">Download</a></td>
</tr>
<tr>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-colorblind.ottytheme"><img src="assets/previews/github-dark-colorblind.svg" alt="GitHub Dark Colorblind"></a><br><b>GitHub Dark Colorblind</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark-colorblind.ottytheme">Download</a></td>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light.ottytheme"><img src="assets/previews/github-light.svg" alt="GitHub Light (classic)"></a><br><b>GitHub Light (classic)</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-light.ottytheme">Download</a></td>
</tr>
<tr>
<td align="center" width="50%"><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark.ottytheme"><img src="assets/previews/github-dark.svg" alt="GitHub Dark (classic)"></a><br><b>GitHub Dark (classic)</b><br><a href="https://github.com/kingsleydon/otty-github-theme/releases/latest/download/github-dark.ottytheme">Download</a></td>
<td></td>
</tr>
</table>

<details>
<summary><b>Use different themes for light and dark mode</b></summary>

In `~/.config/otty/config.toml`:

```toml
theme      = "GitHub Light Default"
theme-dark = "GitHub Dark Default"
```

</details>

<details>
<summary><b>Theme not changing?</b></summary>

Remove any top-level `foreground`, `background` or `palette-N` lines from `~/.config/otty/config.toml`. They override every theme.

</details>

<details>
<summary><b>How the colors are made</b></summary>

Every color is copied from GitHub's VS Code theme, and each line in a theme file names the VS Code key it came from. The sidebar follows VS Code's Explorer, the top tabs follow its editor tabs. Themes don't set a font, so yours is kept.

A [weekly workflow](.github/workflows/update.yml) pulls the latest VS Code theme and opens a pull request when GitHub changes a color. To regenerate by hand:

```sh
sh scripts/update.sh && python3 scripts/preview.py
```

</details>

## License

[MIT](LICENSE). Colors from [primer/github-vscode-theme](https://github.com/primer/github-vscode-theme) (MIT, © Primer). Not affiliated with GitHub or Otty.
