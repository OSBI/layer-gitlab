# Overview
This charm provides the GitLab open source git repo management platform. 

GitLab includes git repository management, code reviews, issue tracking, wikis and much more. 
GitLab comes with GitLab CI, an easy to use continuous integration and deployment tool.

Discuss issues and plan milestones. Do code reviews and make line comments. Mention your colleagues anywhere. View activity streams of projects or people.

GitLab has integrations for tons of tools such as Slack, Hipchat, LDAP, JIRA, Jenkins, many types of hooks and a complete API.

# Usage

To deploy Gitlab simply run:

    juju deploy cs:~f-tom-n/trusty/gitlab
    juju expose gitlab

# Limitations

Curently there is no HA mode or scale out.

# Code

Source Code: https://github.com/osbi/layer-gitlab

Built Charm: https://code.launchpad.net/~f-tom-n/charms/trusty/gitlab/trunk

# Contact Information

- <tom@analytical-labs.com>
