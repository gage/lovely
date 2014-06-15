 #!/bin/bash
 mkdir -p data/lovely
 mongoexport --db lovely --collection auth_group --out data/lovely/auth_group.json
 mongoexport --db lovely --collection auth_group_permissions --out data/lovely/auth_group_permissions.json
 mongoexport --db lovely --collection auth_message --out data/lovely/auth_message.json
 mongoexport --db lovely --collection auth_permission --out data/lovely/auth_permission.json
 mongoexport --db lovely --collection auth_user --out data/lovely/auth_user.json
 mongoexport --db lovely --collection auth_user_groups --out data/lovely/auth_user_groups.json
 mongoexport --db lovely --collection auth_user_user_permissions --out data/lovely/auth_user_user_permissions.json
 mongoexport --db lovely --collection django_admin_log --out data/lovely/django_admin_log.json
 mongoexport --db lovely --collection django_content_type --out data/lovely/django_content_type.json
 mongoexport --db lovely --collection django_session --out data/lovely/django_session.json
 mongoexport --db lovely --collection django_site --out data/lovely/django_site.json
 mongoexport --db lovely --collection news_news --out data/lovely/news_news.json
 mongoexport --db lovely --collection system.indexes --out data/lovely/system.indexes.json

