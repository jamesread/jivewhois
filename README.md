Jive Whois
---

A simple tool to lookup Jive users via command line, it uses the Jive REST API.

Example
---

    user@machine: ./jivewhois.py alice
	+---------------------+--------------------+
	|           Full name | Alice Example      |
	|              E-Mail | alice@redhat.com   |
	|           Job title | Office Manager     |
	|            Location | London Office      |
	|            Timezone | Europe/Dublin      |
	|                 --- | ---                |
	| Mobile Phone Number | 009831235523       |
	|        Pager Number | 1203984            |
	+---------------------+--------------------+


Configuration
---

Create a file called `jivewhois.ini` in your home directory, using this as a template;

    [authentication]
	username=myuser
	password=mypassword
	emailDomain=example.com
	url=https://jive.mysite.com/api/core/v3/people/email/
