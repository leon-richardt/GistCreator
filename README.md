# GistCreator

A dumb wrapper for creating GitHub Gists from the command line.

# Dependencies
* [`requests`](https://pypi.org/project/requests/) for HTTP requests to the GitHub API
* [`pyperclip`](https://pypi.org/project/pyperclip/) (optional) for cross-platform clipboard support

# Usage

**NOTE:** In order to use this script, you need to have a `token.txt` file in the same directory as the script itself.
This file should contain nothing but a [Personal Access Token](https://github.com/settings/tokens).
You only need to check the check box on the `gist` option when creating the token.

This is intended to only be a temporary solution until I figure something nicer.

Basic usage:
```{shell}
python gist_creator.py [--clipboard] [--description <description>]
                       [--public | --secret] [--quiet] <file>...
```

Options:
* `--clipboard`
    * Automatically copy the URL of the created Gist to the clipboard.
* `--description <description>`
    * Set the description of the Gist to \<description\>.
* `--public`
    * Make the created Gist public.
* `--secret`
    * Make the created Gist secret.
* `--quiet`
    * Do not print anything to `stdout`, only error messages will be printed to
      `stderr`.
* `<file>...`
    * Add the given files to the created Gist.
