# Telegram bot to help you invoke Jenkins builds

## How to use
A detailed use case guide will be added

## Configuration

Install dependencies:

    pip3 install -r requirements.txt

Edit the following file:

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

## TODO
- [ ] Build status support  
- [ ] Build Success or fail report

## Contributions
Any mistakes, or additions do the change test and do a pull request.  
Feel free to contact me on telegram if any issues @vjspranav

## Credits

[Jenkins build script taken from Easy as Linux.](https://www.easyaslinux.com/tutorials/devops/how-to-trigger-a-jenkins-job-remotely-from-python-script/)
