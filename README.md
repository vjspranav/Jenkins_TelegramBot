Telegram bot to help you invoke Jenkins builds

## Configuration

Install dependencies:

    pip3 install -r requirements.txt

Create the following file:

`config.json`:

    {
      "jenkins": {
        "host": "jenkins.teamname.com",
        "user": "username",
        "pass": "test12345"
      },
      "telegram": {
        "token": "xxxx"
      }
    }

## Credits

[Jenkins build script taken from Easy as Linux.](https://www.easyaslinux.com/tutorials/devops/how-to-trigger-a-jenkins-job-remotely-from-python-script/)
