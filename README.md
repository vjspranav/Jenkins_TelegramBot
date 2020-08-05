This is a simple Telegram bot that you can use to invoke jenkins build.
You'd need to provide a few details before (edit the script)
Going through the script would help you out with what all changes you need

# Configuration

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


# Will Update the Readme properly soon

Jenkins build script taken from https://www.easyaslinux.com/tutorials/devops/how-to-trigger-a-jenkins-job-remotely-from-python-script/

Hope you find it useful
