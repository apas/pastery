# pastery

**pastery** is a Sublime Text plugin for [pastery][p] - *the sweetest pastebin in the world.*

## Installation

Through [Package Control][pc].

## Usage

### Settings

Pastery requires an API key. Get yours from your [Pastery.net account page][account].

Open the Pastery’s settings in Sublime Text (`Sublime Text 3/4` > `Preferences` > `Package Settings` > `Pastery` > `Settings - User`) and enter the code snippet below replacing `foo` with your API key. Save the file and that’s it.

```json
{
  "api_key": "foo"
}
```

By default, Pastery deletes snippets after 30 days (43200 minutes). If you want to change this, replace the default value of the key `duration` with the desired value in the settings. The value is set in minutes.

```json
{
  "api_key": "foo",
  "duration": "43200"
}
```

**Now you can use Pastery for Sublime Text.**

### Paste

Select any text, hit `cmd` + `option` + `c` or print in your command palette `Pastery: Send to Pastery` and press <kbd>Enter</kbd> → enter the desired name of your snippet in the input panel → <kbd>Enter</kbd> → the pastery link will be ready to be pasted from your clipboard. If you don’t select any text, the entire file will be pasted. The default snippet name is the file name with the extension for saved files and `Untitled` for unsaved buffers.

## License

MIT

[p]: http://pastery.net
[account]: https://www.pastery.net/account/
[pc]: https://packagecontrol.io/packages/Pastery
