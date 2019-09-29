# LSP

[![GitHub release](https://img.shields.io/github/release/tomv564/LSP.svg)](https://github.com/tomv564/LSP/releases) [![Build Status](https://travis-ci.org/tomv564/LSP.svg?branch=master)](https://travis-ci.org/tomv564/LSP) [![Coverage Status](https://coveralls.io/repos/github/tomv564/LSP/badge.svg?branch=master)](https://coveralls.io/github/tomv564/LSP?branch=master) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)]() [![Join the chat at https://gitter.im/SublimeLSP/Lobby](https://badges.gitter.im/SublimeLSP/Lobby.svg)](https://gitter.im/SublimeLSP/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Gives Sublime Text 3 rich editing features for languages with Language Server Protocol support.

Tested against language servers for javascript, typescript, python, php, java, go, c/c++ (clangd), scala (dotty), julia, rust, reason.

See [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) for available implementations.

## Features

Completions with snippet support.

Navigate code with `Go to Symbol Definition` and `Find Symbol References`

Inline documentation from Hover and Signature Help popups

![hover screenshot](https://raw.githubusercontent.com/tomv564/LSP/master/docs/images/screenshot-hover.png)

As-you-type diagnostics with support for code fixes (`F4` to select, `super+.` to trigger actions)

![diagnostics screenshot](https://raw.githubusercontent.com/tomv564/LSP/master/docs/images/screenshot-diagnostics-action.png)


## Installation

### By Package Control

1. Download & Install `Sublime Text 3` (https://www.sublimetext.com/3)
1. Go to the menu `Tools -> Install Package Control`, then,
   wait few seconds until the `Package Control` installation finishes
1. Go to the menu `Preferences -> Package Control`
1. Type `Package Control Add Channel` on the opened quick panel and press <kbd>Enter</kbd>
1. Then, input the following address and press <kbd>Enter</kbd>
   ```
   https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json
   ```
1. Now, go again to the menu `Preferences -> Package Control`
1. This time type `Package Control Install Package` on the opened quick panel and press <kbd>Enter</kbd>
1. Then, search for `LSP` and press <kbd>Enter</kbd>

See also:
1. [ITE - Integrated Toolset Environment](https://github.com/evandrocoan/ITE)
1. [Package control docs](https://packagecontrol.io/docs/usage) for details.


## Configuration

1. Install a language server for a language of your choice
2. Run `LSP: Enable Language Server` from the Command Palette to enable your server.
  * A configuration can be added under `clients` in `Preferences: LSP Settings`
3. Open a document supported by this language server.
4. LSP should report the language server starting in the status bar.

Documentation is available at [LSP.readthedocs.io](https://LSP.readthedocs.io) or [in the docs directory](https://github.com/tomv564/LSP/blob/master/docs/index.md)

## Troubleshooting

Enable the `log_debug` setting, restart Sublime and open the console.
See the [Troubleshooting](https://lsp.readthedocs.io/en/latest/#troubleshooting) guide for tips and known limitations.

Have you added multiple folders to your Sublime workspace? LSP may not handle your second folder as expected, see [this issue](https://github.com/tomv564/LSP/issues/33) for more details.
