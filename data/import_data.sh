 #!/bin/bash
 mongoimport --db lovely --collection auth_group --file lovely/auth_group.json
 mongoimport --db lovely --collection auth_group_permissions --file lovely/auth_group_permissions.json
 mongoimport --db lovely --collection auth_message --file lovely/auth_message.json
 mongoimport --db lovely --collection auth_permission --file lovely/auth_permission.json
 mongoimport --db lovely --collection auth_user --file lovely/auth_user.json
 mongoimport --db lovely --collection auth_user_groups --file lovely/auth_user_groups.json
 mongoimport --db lovely --collection auth_user_user_permissions --file lovely/auth_user_user_permissions.json
 mongoimport --db lovely --collection django_admin_log --file lovely/django_admin_log.json
 mongoimport --db lovely --collection django_content_type --file lovely/django_content_type.json
 mongoimport --db lovely --collection django_session --file lovely/django_session.json
 mongoimport --db lovely --collection django_site --file lovely/django_site.json
 mongoimport --db lovely --collection news_news --file lovely/news_news.json
 mongoimport --db lovely --collection system.indexes --file lovely/system.indexes.json

