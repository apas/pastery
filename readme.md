# pastery

**pastery** is a Sublime Text plugin for [pastery][p] - *the sweetest pastebin in the world.*

## Installation

Through [Package Control][pc].

## Usage

**Do once**:

Pastery requires an API key. Get yours from your [Pastery.net account page][account].

Open the Pastery's settings in Sublime Text (`Sublime Text 2/3` > `Preferences` > `Package Settings` > `Pastery` > `Settings - User`) and enter the code snippet below replacing `foo` with your API key. Save the file and that's it.

    {
      "api_key": "foo"
    }

**Now you can use Pastery for Sublime Text.**

Select any text, hit `cmd` + `option` + `c` and the pastery link will be ready to be pasted from your clipboard.
If you don't select any text, the entire file will be pasted.

## License

MIT

[p]: http://pastery.net
[account]: https://www.pastery.net/account/
[pc]: https://packagecontrol.io/packages/Pastery
