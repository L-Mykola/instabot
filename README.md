# Instagram Mass Engagement Bot

A Python-based tool built on top of [Instagrapi](https://github.com/adw0rd/instagrapi) to automate liking and following actions on Instagram. Supports session persistence, configurable delays, and optional proxy integration for IP rotation.

## Features

- **Session Management**: Automatically loads and saves session files to avoid frequent logins.
- **Rate Limiting**: Randomized delays between actions to mimic human behavior.
- **Action Simulation**: Randomly performs likes or follows on a list of target user IDs.
- **Error Handling**: Gracefully skips users when encountering rate limits, private accounts, or GraphQL errors.
- **Proxy Support**: Optional SOAX proxy integration to rotate IP addresses.
- **Configurable**: All settings (targets, delays, max actions, proxy credentials) are stored in a JSON settings file.

## Requirements

- Python 3.8+
- [Instagrapi](https://pypi.org/project/instagrapi/)
- [Loguru](https://pypi.org/project/loguru/)

## Installation

1. Clone this repository:

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create two JSON files under the `config/` directory:

1. **accounts.json** (list of Instagram credentials):
   ```json
   {
     "credentials": [
       {"username": "user1", "password": "pass1"},
       {"username": "user2", "password": "pass2"}
     ]
   }
   ```

2. **settings.json** (behavior settings):
   ```json
   {
     "target_ids": [123456789, 987654321, ...],
     "max_actions_per_run": 10,
     "min_delay": 5,
     "max_delay": 15,
     "proxy": {
        "set_proxy": false,
        "proxy_url": "YOUR_PROXY_URL"
      }
   }
   ```

- `target_ids`: List of Instagram user IDs to like/follow.
- `max_actions_per_run`: Maximum number of actions per account per run.
- `min_delay` / `max_delay`: Delay range (in seconds) between actions.
- `proxy`: Set to `true` to enable SOAX proxy.
- `proxy_url`: proxy credentials and connection details.

## Usage

Run the main script:

```bash
python main.py
```

This will:

1. Load settings and account credentials.
2. For each account:
   - Attempt to load an existing session (`sessions/{username}_session.json`).
   - If the session is invalid or missing, log in with username & password and save a new session file.
   - Optionally configure the proxy if enabled.
   - Perform randomized like/follow actions on the configured `target_ids`.
   - Log out and proceed to the next account.


## Logging

This tool uses [Loguru](https://github.com/Delgan/loguru) for logging. By default, it logs info and warning messages to the console. You can configure Loguru in `src/user/user.py` or redirect logs to a file as needed.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

