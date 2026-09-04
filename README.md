:information_source: You are reading the README of the `main` branch. This branch targets ST4. If you are looking for the ST3 version, switch to the [st3 branch](https://github.com/sublimelsp/LSP/tree/st3).

<p>
  <h1 align="center">LSP</h1>
</p>

<p align="center">
  <a href="https://github.com/sublimelsp/LSP/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/sublimelsp/LSP">
  </a>
  <a href="https://github.com/sublimelsp/LSP/releases">
    <img src="https://img.shields.io/github/release/sublimelsp/LSP.svg">
  </a>
  <a href="https://lsp.sublimetext.io">
    <img src="https://img.shields.io/badge/docs-ST4-blue">
  </a>
  <a href="#chat">
    <img src="https://img.shields.io/discord/280102180189634562?label=SublimeHQ%20Discord&logo=discord">
  </a>
  <br>
</p>

<p align="center">Like an IDE, except it's the good parts. <a href="https://lsp.sublimetext.io">Learn more</a>.</p>

<p align="center"><img src="docs/src/images/showcase.gif" alt="TypeScript Server Example"></img></p>

## Installation

### Stable Version

Open the command palette and run `Package Control: Install Package`, then select `LSP`.

### Development Version

Clone this repository into your Packages directory. Open the command palette and run `Package Control: Satisfy Dependencies`.

## Getting started

Follow the installation steps for a [specific language server](https://lsp.sublimetext.io/language_servers).

Open a document supported by the language server. LSP should report the language server starting in the status bar.

See more information in the [documentation](https://lsp.sublimetext.io) :open_book:.

## Getting help

If you have any problems, see the [troubleshooting](https://sublimelsp.github.io/LSP/troubleshooting/) guide for tips and known limitations. If the documentation cannot solve your problem, you can look for help in:
<a name="chat"></a>

* The [#lsp](https://discordapp.com/channels/280102180189634562/645268178397560865) channel (join the [SublimeHQ Discord](https://discord.gg/TZ5WN8t) first!)
* By [searching or creating a new issue](https://github.com/sublimelsp/LSP/issues)

## Installation

### By Package Control

1. Download & Install **`Sublime Text 3`** (https://www.sublimetext.com/3)
1. Go to the menu **`Tools -> Install Package Control`**, then,
    wait few seconds until the installation finishes up
1. Now,
    Go to the menu **`Preferences -> Package Control`**
1. Type **`Add Channel`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
    input the following address and press <kbd>Enter</kbd>
    ```
    https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json
    ```
1. Go to the menu **`Tools -> Command Palette...
    (Ctrl+Shift+P)`**
1. Type **`Preferences:
    Package Control Settings – User`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
    find the following setting on your **`Package Control.sublime-settings`** file:
    ```js
    "channels":
    [
        "https://packagecontrol.io/channel_v3.json",
        "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
    ],
    ```
1. And,
    change it to the following, i.e.,
    put the **`https://raw.githubusercontent...`** line as first:
    ```js
    "channels":
    [
        "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
        "https://packagecontrol.io/channel_v3.json",
    ],
    ```
    * The **`https://raw.githubusercontent...`** line must to be added before the **`https://packagecontrol.io...`** one, otherwise,
      you will not install this forked version of the package,
      but the original available on the Package Control default channel **`https://packagecontrol.io...`**
    > [!WARNING]
    > Placing this custom channel before the default channel changes Package Control's resolution globally. Packages from this channel with the same name will override versions from the default channel.
    >
    > You can review the channel contents here:
    > https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json
1. Now,
    go to the menu **`Preferences -> Package Control`**
1. Type **`Install Package`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
    search for **`LSP`** and press <kbd>Enter</kbd>

See also:

1. [ITE - Integrated Toolset Environment](https://github.com/evandrocoan/ITE)
1. [Package control docs](https://packagecontrol.io/docs/usage) for details.
